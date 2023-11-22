import time
import os
import sys
from planner import Action
from vessel_state import VesselState, State
from utils import PlannerType
from replanner import *

class PlanExecutor():

    def __init__(self, vessel: VesselState, plannerType: PlannerType):
        self.vessel = vessel
        self.plannerType = plannerType

    def executePlan(self):
        actions = self.vessel.allActions
        for a in actions:
            try:
                self.executeAction(a)
            except KeyboardInterrupt:
                print('\nReplanning')
                makeProblemFile(self.vessel, plannerType=self.plannerType)
                os.system('python3 main.py True')
                sys.exit()
            self.vessel.updateActions(a)
            self.vessel.updatePredEnd(a)

    def executeAction(self, a: Action):
        action  = a.getAction()
        pred    = a.getPredicates()
        start   = a.getStartTime()

        if action == "transit":
            self.vessel.updateState(State.IN_TRANSIT)
            if self.plannerType == PlannerType.TEMPORAL:
                self.vessel.updatePredStart(a)

            portFrom    = pred[0]
            portTo      = pred[1]
            print("At %f\n Transit from %s to %s\n" % (start, portFrom, portTo))
            time.sleep(3)

        elif action == "undock":
            self.vessel.updateState(State.UNDOCKING)
            if self.plannerType == PlannerType.TEMPORAL:
                self.vessel.updatePredStart(a)

            port = pred[0]
            print("At %f\n Undocking at %s\n" % (start, port))
            time.sleep(3)

        elif action == "dock":
            self.vessel.updateState(State.DOCKING)
            if self.plannerType == PlannerType.TEMPORAL:
                self.vessel.updatePredStart(a)

            port = pred[0]
            print("At %f\n Docking at %s\n" % (start, port))
            time.sleep(3)

        elif action == "load" or action == "start-load" or action == "end-load":
            self.vessel.updateState(State.DOCKED)
            if self.plannerType == PlannerType.TEMPORAL:
                self.vessel.updatePredStart(a)

            port = pred[0]
            goods = pred[1]
            print("At %f\n Loading %s at %s\n" % (start, goods, port))
            time.sleep(3)

        elif action == "unload" or action == "start-unload" or action == "end-unload":
            self.vessel.updateState(State.DOCKED)
            if self.plannerType == PlannerType.TEMPORAL:
                self.vessel.updatePredStart(a)

            port = pred[0]
            goods = pred[1]
            print("At %f\n Unloading %s at %s\n" % (start, goods, port))
            time.sleep(3)

        elif action == "fuelling":
            self.vessel.updateState(State.DOCKED)
            if self.plannerType == PlannerType.TEMPORAL:
                self.vessel.updatePredStart(a)

            port = pred[0]
            print("At %f\n Fuelling at %s\n" % (start, port))
            time.sleep(3)

        else:
            raise Exception("Not a valid action name")