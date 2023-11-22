from planner import Action
from vessel_state import VesselState, State
from utils import PlannerType
import time
from replanner import *

class PlanExecutor():

    def __init__(self, vessel: VesselState, plannerType: PlannerType):
        self.vessel = vessel
        self.plannerType = plannerType

    def executePlan(self):
        actions = self.vessel.allActions
        for a in actions:
            self.executeAction(a)
            self.vessel.updateActions(a)
            self.vessel.updatePredEnd(a)

    def executeAction(self, a: Action):
        action  = a.getAction()
        pred    = a.getPredicates()
        start   = a.getStartTime()
        end     = a.getEndTime()
        dur     = a.getDuration()

        if action == "transit":
            self.vessel.updateState(State.IN_TRANSIT)
            if self.plannerType == PlannerType.TEMPORAL:
                self.vessel.updatePredStart(a)

            portFrom    = pred[0]
            portTo      = pred[1]
            print("At %f\n Transit from %s to %s\n" % (start, portFrom, portTo))
            time.sleep(2)

            print("Vessel in state %s\n" % self.vessel.state)

        elif action == "undock":
            self.vessel.updateState(State.UNDOCKING)
            if self.plannerType == PlannerType.TEMPORAL:
                self.vessel.updatePredStart(a)

            port = pred[0]
            print("At %f\n Undocking at %s\n" % (start, port))
            time.sleep(1)

            print("Vessel in state %s\n" % self.vessel.state)

        elif action == "dock":
            self.vessel.updateState(State.DOCKING)
            if self.plannerType == PlannerType.TEMPORAL:
                self.vessel.updatePredStart(a)

            port = pred[0]
            print("At %f\n Docking at %s\n" % (start, port))
            time.sleep(1)

            print("Vessel in state %s\n" % self.vessel.state)

        elif action == "load" or action == "start-load" or action == "end-load":
            self.vessel.updateState(State.DOCKED)
            if self.plannerType == PlannerType.TEMPORAL:
                self.vessel.updatePredStart(a)

            port = pred[0]
            goods = pred[1]
            print("At %f\n Loading %s at %s\n" % (start, goods, port))
            time.sleep(1)

            print("Vessel in state %s\n" % self.vessel.state)

        elif action == "unload" or action == "start-unload" or action == "end-unload":
            self.vessel.updateState(State.DOCKED)
            if self.plannerType == PlannerType.TEMPORAL:
                self.vessel.updatePredStart(a)

            port = pred[0]
            goods = pred[1]
            print("At %f\n Unloading %s at %s\n" % (start, goods, port))
            time.sleep(1)

            print("Vessel in state %s\n" % self.vessel.state)

        elif action == "fuelling":
            self.vessel.updateState(State.DOCKED)
            if self.plannerType == PlannerType.TEMPORAL:
                self.vessel.updatePredStart(a)

            port = pred[0]
            print("At %f\n Fuelling at %s\n" % (start, port))
            time.sleep(1)

            print("Vessel in state %s\n" % self.vessel.state)

            ### Testing replanning at this step
            fileName = '/home/marie/project_thesis/Planning/replan_problem.pddl'
            makeProblemFile(self.vessel, fileName, plannerType=self.plannerType)


        else:
            raise Exception("Not a valid action name")