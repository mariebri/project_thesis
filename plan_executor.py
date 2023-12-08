import copy
import matplotlib.pyplot as plt
import math
import os
import sys
import time

from control import Control
from planner import Action, Planner
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
        self.allActions         = self.remainingActions + self.finishedActions

        self.vesselState        = VesselState(battery=self.plan.battery, replan=self.plan.replan, scenario=self.plan.scenario)
        self.control            = control

        self.time               = 0
        self.N                  = N
        self.n                  = 0

        self.eta_sim            = np.zeros((3,self.N))
        self.nu_sim             = np.zeros((3,self.N))
        self.tau_sim            = np.zeros((3,self.N))

    def executePlan(self):
        actions = self.allActions
        for a in actions:

            if a.hasConcurrent:
                print('Action %s has a concurrent action!' % a.action)

            try:
                self.executeAction(a)
                self.updateActions(a)
                self.updatePredEnd(a)

                if self.plan.scenario == 3:
                    self.vesselState.checkBattery()
            except KeyboardInterrupt:
                print('\nReplanning')
                replanner = Replanner(self.init, self.goal, self.plan.planner, self.plan.scenario)
                replanner.makeProblemFile(low_battery=self.vesselState.low_battery, port=self.vesselState.port)
                
                b   = self.vesselState.battery
                eta = self.control.vessel.eta
                x, y, p = eta[0], eta[1], eta[2]
                os.system('python3 main.py -r 1 -b %s -x %s -y %s -p %s' % (b, x, y, p))
                sys.exit()

    def executeAction(self, a: Action):
        action  = a.action
        pred    = a.parameters
        start   = a.start

        if action == "transit":
            portFrom, portTo = getPortName(pred[0], pred[1])
            print("At %f\n Transit from %s to %s\n" % (start, portFrom, portTo))

            self.vesselState.updateState(State.IN_TRANSIT, portTo)
            self.updatePredStart(a)

            self.executeTransit(portFrom, portTo)

        elif action == "undock":
            port, areaTo = getPortName(pred[0], state=State.UNDOCKING)
            print("At %f\n Undocking at %s\n" % (start, port))

            self.vesselState.updateState(State.UNDOCKING, port)
            self.updatePredStart(a)

            self.executeTransit(port, areaTo, transit=False)

        elif action == "dock":
            areaFrom, port = getPortName(pred[0], state=State.DOCKING)
            print("At %f\n Docking at %s\n" % (start, port))

            self.vesselState.updateState(State.DOCKING, port)
            self.updatePredStart(a)

            self.executeTransit(areaFrom, port, transit=False)
            self.vesselState.updateState(State.DOCKED, port)

        elif action == "load":
            port = pred[0]
            goods = pred[1]
            print("At %f\n Loading %s at %s\n" % (start, goods, port))

            self.vesselState.updateState(State.DOCKED, port)
            self.updatePredStart(a)

            for i in range(math.floor(a.dur/self.control.h)):
                self.n     += 1
                self.time  += self.control.h
                if i % 25 == 0:
                    time.sleep(1)

        elif action == "unload":
            port = pred[0]
            goods = pred[1]
            print("At %f\n Unloading %s at %s\n" % (start, goods, port))

            self.vesselState.updateState(State.DOCKED, port)
            self.updatePredStart(a)

            for i in range(math.floor(a.dur/self.control.h)):
                self.n     += 1
                self.time  += self.control.h
                if i % 25 == 0:
                    time.sleep(1)

        elif action == "charging":
            port = pred[0]
            print("At %f\n Charging at %s\n" % (start, port))

            self.vesselState.updateState(State.DOCKED, port)
            self.updatePredStart(a)

            for i in range(math.floor(a.dur/self.control.h)):
                self.n     += 1
                self.time  += self.control.h

                # Battery charging every 10 seconds
                battery_sec = math.floor(10/self.control.h)
                if i % battery_sec == 0:
                    self.vesselState.updateBattery(20)
                    print('Charging: %s' % str(self.vesselState.battery))
                    time.sleep(0.5)

        else:
            raise Exception("Not a valid action name")
        
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

    def executeTransit(self, portFrom, portTo, transit=True):
        if not transit:
            eta_d   = self.control.getOptimalEta(portFrom, portTo, step=3)
        else:
            eta_d   = self.control.getOptimalEta(portFrom, portTo)
        l_eta_d = eta_d.shape[1]

        i = 0
        if l_eta_d == 1:
            return
        
        wp1 = eta_d[:2,i]
        wp2 = eta_d[:2,i+1]
        for n in range(self.n, self.N):

            if inProximity(wp2, self.control.vessel.eta[:2], self.control.roa):
                if i == l_eta_d-2:
                    break
                i  += 1
                wp1 = eta_d[:2,i]
                wp2 = eta_d[:2,i+1]

            chi_d           = self.control.LOSguidance(wp1, wp2)
            psi_d           = chi_d - self.control.vessel.getCrabAngle()
            eta, nu, tau    = self.control.headingAutopilot(psi_d, wp2)

            # Storing simulation parameters
            self.eta_sim[:,n]    = eta
            self.nu_sim[:,n]     = nu
            self.tau_sim[:,n]    = tau.reshape(3)

            # Battery level decreasing every 30 seconds:
            if self.plan.scenario == 3:
                battery_sec = math.floor(30/self.control.h)
                if n % battery_sec == 0:
                    self.vesselState.updateBattery(-1)
                    print('Battery level decreasing by 1: %s' % str(self.vesselState.battery))

            # Plot vessel every 10 seconds:
            plot_sec = math.floor(10/self.control.h)
            if n % plot_sec == 0:
                self.control.vessel.plot()
                plt.pause(0.01)

            self.n      += 1
            self.time   += self.control.h

        