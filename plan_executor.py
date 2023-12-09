import copy
import matplotlib.pyplot as plt
import math
import os
import sys
import time

from control import Control
from planner import Action, ConcurrentAction, Planner
from replanner import Replanner
from vessel_state import VesselState
from utils import *

class PlanExecutor:
    def __init__(self, plan: Planner, control: Control, N):
        self.plan               = plan
        self.init, self.goal    = self.plan.getPredicates()
        self.port0              = self.plan.getStartPos()

        self.remainingActions   = copy.deepcopy(self.plan.actions)
        self.finishedActions    = []
        self.allActions         = self.finishedActions + self.remainingActions
        self.concurrentActions  = self.plan.concurrentActions

        self.vesselState        = VesselState(scenario=self.plan.scenario)
        self.control            = control

        # Simulation parameters
        self.time               = 0
        self.n                  = 0
        self.N                  = N

        self.aIdx               = 0
        self.eta_d              = np.zeros((3,1))
        self.wp1, self.wp2      = [], []
        self.etaIdx             = 0
        self.etaIdxMax          = self.eta_d.shape[1]-2
        self.newRoute           = False
        self.hardLimit          = True

        self.eta_sim            = np.zeros((3,self.N))
        self.nu_sim             = np.zeros((3,self.N))
        self.tau_sim            = np.zeros((3,self.N))
        self.U_sim              = np.zeros(self.N)
            
    def updateActions(self, finishedAction: Action):
        self.remainingActions.remove(finishedAction)
        self.finishedActions.append(finishedAction)

    def updatePredStart(self, startedAction: Action):
        if self.plan.planner == PlannerType.TEMPORAL:
            # Only used for temporal planners
            addEffects, delEffects = startedAction.getEffects()
            addEffects = addEffects[0]
            delEffects = delEffects[0]

            # Update
            effInPred = [False for i in range(len(addEffects))]
            for pred in self.init:
                for i in range(len(addEffects)):
                    if pred == addEffects[i]:
                        effInPred[i] = True
                for eff in delEffects:
                    if pred == eff:
                        self.init.remove(pred)
            
            for i in range(len(effInPred)):
                if not effInPred[i]:
                    self.init.append(addEffects[i])

            for pred in self.goal:
                for eff in addEffects:
                    if pred == eff:
                        self.goal.remove(pred)
        else:
            return

    def updatePredEnd(self, finishedAction: Action):
        addEffects, delEffects = finishedAction.getEffects()

        if self.plan.planner == PlannerType.TEMPORAL:
            addEffects = addEffects[1]
            delEffects = delEffects[1]

        # Update
        effInPred = [False for i in range(len(addEffects))]
        for pred in self.init:
            for i in range(len(addEffects)):
                if pred == addEffects[i]:
                    effInPred[i] = True
            for eff in delEffects:
                if pred == eff:
                    self.init.remove(pred)
        
        for i in range(len(effInPred)):
            if not effInPred[i]:
                self.init.append(addEffects[i])

        for pred in self.goal:
            for eff in addEffects:
                if pred == eff:
                    self.goal.remove(pred)

    def updateStartedAction(self, a: Action, state):
        if a.isStarted:
            return
        
        port, port2 = getPortName(a.parameters[0])
        if state == State.IN_TRANSIT:
            _, port = getPortName(a.parameters[0], a.parameters[1])
        if state == State.DOCKING:
            port = port2
        
        self.vesselState.updateState(state, port)
        self.updatePredStart(a)
        a.isStarted = True

    def executeAction(self, a: Action):

        if a.action == "transit":
            self.hardLimit = False
            if not a.isStarted:
                self.newRoute = True
            self.updateStartedAction(a, State.IN_TRANSIT)
            portFrom, portTo    = getPortName(a.parameters[0], a.parameters[1])
            self.executeTransit(a, portFrom, portTo, step=5)

        elif a.action == "undock":
            self.hardLimit = False
            if not a.isStarted:
                self.newRoute = True
            self.updateStartedAction(a, State.UNDOCKING)
            port, areaTo = getPortName(a.parameters[0], state=State.UNDOCKING)
            self.executeTransit(a, port, areaTo, step=3)

        elif a.action == "dock":
            self.hardLimit = False
            if not a.isStarted:
                self.newRoute = True
            self.updateStartedAction(a, State.DOCKING)
            areaFrom, port = getPortName(a.parameters[0], state=State.DOCKING)
            self.executeTransit(a, areaFrom, port, step=3)

        elif a.action == "load":
            self.updateStartedAction(a, State.DOCKED)
            self.executeDocked()
            self.hardLimit = True

        elif a.action == "unload":
            self.updateStartedAction(a, State.DOCKED)
            self.executeDocked()
            self.hardLimit = True

        elif a.action == "charging":
            self.updateStartedAction(a, State.DOCKED)
            self.executeDocked()
            self.hardLimit = True

            battery_sec = math.floor(10/self.control.h)
            if self.n % battery_sec == 0:
                self.vesselState.updateBattery(20)
                print('Charging: %s' % str(self.vesselState.battery))

        else:
            raise Exception("Not a valid action name")
        
        if self.n % 50 == 0:
                a.print()
        
        a.update(self.control.h, self.hardLimit)

    def executeTransit(self, a: Action, portFrom, portTo, step):
        if self.newRoute:
            self.newRoute = False
            self.eta_d          = self.control.getOptimalEta(portFrom, portTo, step)
            self.etaIdxMax      = self.eta_d.shape[1]-2

            if self.etaIdxMax <= 0:
                a.isExecuted = True
                return
            self.etaIdx         = 0
            self.wp1            = self.eta_d[:2, 0]
            self.wp2            = self.eta_d[:2, 1]

        if self.control.inProximity(self.wp2):
            if self.etaIdx == self.etaIdxMax:
                a.isExecuted = True
                return
            self.etaIdx += 1
            self.wp1    = self.eta_d[:2, self.etaIdx]
            self.wp2    = self.eta_d[:2, self.etaIdx+1]

        chi_d           = self.control.LOSguidance(self.wp1, self.wp2)
        psi_d           = chi_d - self.control.vessel.getCrabAngle()
        eta, nu, tau    = self.control.headingAutopilot(psi_d, self.wp2)
        U               = np.sqrt(nu[0]**2 + nu[1]**2)

        # Storing simulation parameters
        self.eta_sim[:,self.n]  = eta
        self.nu_sim[:,self.n]   = nu
        self.tau_sim[:,self.n]  = tau.reshape(3)
        self.U_sim[self.n]      = U

        # Battery level decreasing every 30 seconds:
        if self.plan.scenario == 3:
            battery_sec = math.floor(30/self.control.h)
            if self.n % battery_sec == 0:
                self.vesselState.updateBattery(-1)
        return

    def executeDocked(self):
        # Storing simulation parameters
        self.eta_sim[:,self.n]  = self.control.vessel.eta
        self.nu_sim[:,self.n]   = self.control.vessel.nu
        self.tau_sim[:,self.n]  = np.zeros(3)
        self.U_sim[self.n]      = 0

    def replanning(self):
        replanner = Replanner(self.init, self.goal, self.plan, self.vesselState.battery, \
                                  self.vesselState.lowBattery, self.vesselState.port, self.control.vessel.eta)
        self.plan   = replanner.plan
        self.init   = replanner.plan.init
        self.goal   = replanner.plan.goal
        self.port0  = replanner.plan.getStartPos()
        
        self.remainingActions   = copy.deepcopy(replanner.plan.actions)
        self.finishedActions    = []
        self.allActions         = self.finishedActions + self.remainingActions
        self.concurrentActions  = replanner.plan.concurrentActions
        self.aIdx               = 0

    def simulationLoop(self):
        actions = self.allActions

        try:
            while self.n <= self.N:
                a = actions[self.aIdx]
                
                # Executing concurrent actions
                if a.hasConcurrent:
                    ca = a.concurrentAction

                    for a in ca.active:
                        self.executeAction(a)

                        if a.isExecuted:
                            self.updateActions(a)
                            self.updatePredEnd(a)
                            ca.updateActive(a)

                            if len(ca.active) == 0:
                                self.aIdx += len(ca.actions)

                # Executing single actions
                else:
                    self.executeAction(a)

                    if a.isExecuted:
                        self.updateActions(a)
                        self.updatePredEnd(a)
                        self.aIdx += 1

                # Update n and time
                self.n     += 1
                self.time  += self.control.h

                # Check if all actions are finished
                if len(self.remainingActions) == 0:
                    return

        except NameError:
            self.vesselState.replan = True
            self.replanning()
            self.simulationLoop()