import copy
import math
import matplotlib.pyplot as plt

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
        self.area0              = self.port0 + "-port"

        self.remainingActions   = copy.deepcopy(self.plan.actions)
        self.finishedActions    = []
        self.allActions         = self.finishedActions + self.remainingActions
        self.concurrentActions  = self.plan.concurrentActions

        self.vesselState        = VesselState(scenario=self.plan.scenario, toArea=self.area0)
        self.control            = control

        # Simulation parameters
        self.time               = 0
        self.n                  = 0
        self.nReplan            = N
        self.N                  = N

        self.aIdx               = 0
        self.eta_d              = np.zeros((3,1))
        self.eta_toArea         = self.port0
        self.wp1, self.wp2      = [], []
        self.etaIdx             = 0
        self.etaIdxMax          = self.eta_d.shape[1]-2
        self.newRoute           = False
        self.hardLimit          = True

        self.eta_sim            = np.zeros((3,self.N))
        self.nu_sim             = np.zeros((3,self.N))
        self.f_sim              = np.zeros((3,self.N))
        self.etad_sim           = np.zeros((3,self.N))
        self.track_err          = np.zeros((2,self.N))
            
    def updateActions(self, finishedAction: Action):
        """
        Remove finished action from remaining actions set and
        append to finished actions set.

        If the duration of the action differs from the original plan,
        update start time of all upcoming actions.
        """

        self.remainingActions.remove(finishedAction)
        self.finishedActions.append(finishedAction)

        if finishedAction.durDiff != 0.0:
            print(finishedAction.action, 'duration difference:', finishedAction.durDiff)
            for a in self.remainingActions:
                a.start += finishedAction.durDiff

    def updatePredStart(self, startedAction: Action):
        """
        Goal: Update effects that are set at start of the action
        
        Only used for temporal planners to update effects "at start"
        """
        
        if self.plan.planner == PlannerType.TEMPORAL:
            addEffects, delEffects = startedAction.getEffects()
            addEffects = addEffects[0]
            delEffects = delEffects[0]

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
        """
        Goal: Update effects that are set at end of action

        Used for both classical and temporal planners
        """
        
        addEffects, delEffects = finishedAction.getEffects()

        if self.plan.planner == PlannerType.TEMPORAL:
            addEffects = addEffects[1]
            delEffects = delEffects[1]

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
        """
        Goal: Update vessel state and initial predicates at start of action
        """

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
        """
        Executes one step of a given action
        """

        if a.action == "transit":
            self.hardLimit = False
            if not a.isStarted:
                self.newRoute = True
            self.updateStartedAction(a, State.IN_TRANSIT)
            portFrom, portTo    = getPortName(a.parameters[0], a.parameters[1])
            self.executeTransit(a, portFrom, portTo)
            a.update(self.control.h, self.hardLimit)

        elif a.action == "undock":
            self.hardLimit = False
            if not a.isStarted:
                self.newRoute = True
            self.updateStartedAction(a, State.UNDOCKING)
            port, areaTo = getPortName(a.parameters[0], state=State.UNDOCKING)
            self.executeTransit(a, port, areaTo, step=3, transit=False)
            a.update(self.control.h, self.hardLimit)

        elif a.action == "dock":
            self.hardLimit = False
            if not a.isStarted:
                self.newRoute = True
            self.updateStartedAction(a, State.DOCKING)
            areaFrom, port = getPortName(a.parameters[0], state=State.DOCKING)
            self.executeTransit(a, areaFrom, port, step=3, transit=False)
            a.update(self.control.h, self.hardLimit)

            if self.plan.scenario == 2 and areaFrom == "D" and a.isExecuted:
                print("Oh no, charging station at port D is busy!")
                self.updateActions(a)
                self.updatePredEnd(a)
                raise NameError("Replanning to find another charging station")

        elif a.action == "load":
            self.updateStartedAction(a, State.DOCKED)
            self.executeDocked()
            self.hardLimit = True
            a.update(self.control.h, self.hardLimit)

        elif a.action == "unload":
            self.updateStartedAction(a, State.DOCKED)
            self.executeDocked()
            self.hardLimit = True
            a.update(self.control.h, self.hardLimit)

        elif a.action == "charging":
            self.updateStartedAction(a, State.DOCKED)
            self.executeDocked()
            self.hardLimit = True
            a.update(self.control.h, self.hardLimit)

            battery_sec = math.floor(10/self.control.h)
            if self.n % battery_sec == 0:
                self.vesselState.updateBattery(20)
                print('Charging: %s' % str(self.vesselState.battery))

        else:
            raise Exception("Not a valid action name")
        
        if self.n % 50 == 0:
                a.print()

    def executeTransit(self, a, portFrom, portTo, step=5, transit=True):
        """
        Goal: Execute one step of transit

        Finds new route if necessary, and steers vessel towards next waypoint
        """
        if self.newRoute:
            portFrom                    = self.vesselState.toArea
            self.newRoute               = False
            self.eta_d, self.eta_toArea = self.control.getOptimalEta(portFrom, portTo, step)
            self.etaIdxMax              = self.eta_d.shape[1]-2

            if self.etaIdxMax <= 0:
                a.isExecuted = True
                return
            self.etaIdx         = 0
            self.wp1            = self.eta_d[:2, 0]
            self.wp2            = self.eta_d[:2, 1]

        if self.eta_toArea[self.etaIdx] != '':
            self.vesselState.toArea = self.eta_toArea[self.etaIdx]

        if self.control.inProximity(self.wp2, transit):
            if self.etaIdx == self.etaIdxMax:
                a.isExecuted = True
                return
            self.etaIdx += 1
            self.wp1    = self.eta_d[:2, self.etaIdx]
            self.wp2    = self.eta_d[:2, self.etaIdx+1]

        chi_d, track_err    = self.control.LOSguidance(self.wp1, self.wp2)
        psi_d               = chi_d - self.control.vessel.getCrabAngle()
        eta, nu, f          = self.control.headingAutopilot(psi_d, self.wp2, transit)

        # Storing simulation parameters
        self.eta_sim[:,self.n]      = eta
        self.nu_sim[:,self.n]       = nu
        self.f_sim[:,self.n]        = f.reshape(3)
        self.etad_sim[:,self.n]     = self.eta_d[:,self.etaIdx+1]
        self.track_err[:,self.n]    = track_err

        # Battery level decreasing every 25 seconds:
        battery_sec = math.floor(25/self.control.h)
        if self.n % battery_sec == 0:
            self.vesselState.updateBattery(-1)
        return

    def executeDocked(self):
        """
        Execute one step of vessel being docked.
        Only storing simulation parameters.
        """

        self.eta_sim[:,self.n]  = self.control.vessel.eta
        self.nu_sim[:,self.n]   = self.control.vessel.nu
        self.etad_sim[:,self.n] = self.control.vessel.eta

    def replanning(self):
        """
        Makes a new problem file and a new Planner instance based on vessel's current state
        Updates parameters of the PlanExecutor instance.
        """

        self.nReplan= self.n
        replanner = Replanner(self.init, self.goal, self.plan, self.vesselState.battery, \
                                  self.vesselState.lowBattery, self.vesselState.port)
        self.plan   = replanner.plan
        self.init   = replanner.plan.init
        self.goal   = replanner.plan.goal
        self.port0  = replanner.plan.getStartPos()
        self.area0  = self.vesselState.toArea
        self.vesselState.replan = True
        
        self.remainingActions   = copy.deepcopy(replanner.plan.actions)
        self.finishedActions    = []
        self.allActions         = self.finishedActions + self.remainingActions
        self.concurrentActions  = replanner.plan.concurrentActions
        self.aIdx               = 0

    def simulation(self):
        """
        Main simulation loop
        """

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
                    self.N = self.n
                    return
                
                if self.n == self.N:
                    return

        except NameError:
            self.vesselState.replan = True
            self.replanning()
            self.simulation()