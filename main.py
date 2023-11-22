from planner import *
from utils import *
from plan_executor import PlanExecutor
from vessel_state import VesselState

def mainPlanner():
    # Specify the planner type, domain and problem files, and the algorithm
    plannerType = PlannerType.GRAPHPLAN
    replan      = True
    algorithm   = "stp-3"

    # Computing a plan, retrieving a list of the actions
    plan    = Plan(plannerType, algorithm, replan)
    actions = plan.getActions()
    init, goal = plan.getPredicates()
    print("\n\nComputation time: ", plan.computationTime)

    # Declaring a vessel and a plan executor
    vessel  = VesselState(plan, remainingActions=actions, initPred=init, goalPred=goal)
    planExe = PlanExecutor(vessel, plannerType)

    # Executing the plan
    planExe.executePlan()



if __name__ == '__main__':
    mainPlanner()