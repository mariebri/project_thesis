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
    def __init__(self, plan: Planner, control: Control):
        self.plan   = plan
        self.time   = 0

        self.init, self.goal, self.port0 = self.plan.getPredicates(startPos=True)

        self.remainingActions   = copy.deepcopy(self.plan.actions)
        self.finishedActions    = []
        self.allActions         = self.remainingActions + self.finishedActions

        self.vesselState    = VesselState(battery=self.plan.battery, replan=self.plan.replan, scenario=self.plan.scenario)
        self.control        = control

    def executePlan(self):
        actions = self.allActions
        for a in actions:
            try:
                self.executeAction(a)
            except KeyboardInterrupt:
                print('\nReplanning')
                replanner = Replanner(self.init, self.goal, self.plan.planner, self.plan.scenario)
                self.vesselState.print()

                if self.vesselState.low_battery:
                    print('Low battery...')
                    print('Planning for an additional charging stop')
                    replanner.makeProblemFile(low_battery=True, port=self.vesselState.port)
                    os.system('python3 main.py -r True -b %s' % self.vesselState.battery)
                    sys.exit()
                
                replanner.makeProblemFile()
                os.system('python3 main.py -r True -b 100')
                sys.exit()
            self.updateActions(a)
            self.updatePredEnd(a)

    def executeAction(self, a: Action):
        action  = a.getAction()
        pred    = a.getParameters()
        start   = a.getStartTime()

        if action == "transit":
            portFrom, portTo = getPortName(pred[0], pred[1])
            print("At %f\n Transit from %s to %s\n" % (start, portFrom, portTo))

            self.vesselState.updateState(State.IN_TRANSIT, portTo)
            self.updatePredStart(a)

            """
            for i in range(math.floor((a.dur/30)):
                self.vesselState.updateBattery(-1)
                time.sleep(0.5)
            """

            time.sleep(5)

            self.executeTransit(portFrom, portTo)

        elif action == "undock":
            port, areaTo = getPortName(pred[0], state=State.UNDOCKING)
            print("At %f\n Undocking at %s\n" % (start, port))

            self.vesselState.updateState(State.UNDOCKING, port)
            self.updatePredStart(a)

            """
            for i in range(1):
                self.vesselState.updateBattery(-5)
                time.sleep(1)
            """

            time.sleep(5)

            self.executeTransit(port, areaTo)

        elif action == "dock":
            areaFrom, port = getPortName(pred[0], state=State.DOCKING)
            print("At %f\n Docking at %s\n" % (start, port))

            self.vesselState.updateState(State.DOCKING, port)
            self.updatePredStart(a)

            """
            for i in range(1):
                self.vesselState.updateBattery(-5)
                time.sleep(1)
            """

            self.executeTransit(areaFrom, port)

        elif action == "load":
            port = pred[0]
            goods = pred[1]
            print("At %f\n Loading %s at %s\n" % (start, goods, port))

            self.vesselState.updateState(State.DOCKED, port)
            self.updatePredStart(a)

            time.sleep(1)

        elif action == "unload":
            port = pred[0]
            goods = pred[1]
            print("At %f\n Unloading %s at %s\n" % (start, goods, port))

            self.vesselState.updateState(State.DOCKED, port)
            self.updatePredStart(a)

            time.sleep(1)

        elif action == "charging":
            port = pred[0]
            print("At %f\n Charging at %s\n" % (start, port))

            self.vesselState.updateState(State.DOCKED, port)
            self.updatePredStart(a)

            for i in range(5):
                self.vesselState.updateBattery(20)
                time.sleep(1)

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

    def executeTransit(self, portFrom, portTo):
        self.time = self.control.moveVessel(portFrom, portTo, self.time)
        