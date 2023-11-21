from planner import *
from plan_executor import PlanExecutor
from vessel_state import VesselState
from utils import getDomainProblemFiles

def mainPlanner():
    # Specify the planner type, domain and problem files, and the algorithm
    plannerType = PlannerType.TEMPORAL
    replan      = False
    algorithm   = "stp-2"
    domainFile, problemFile = getDomainProblemFiles(plannerType, replan)

    # Computing a plan, retrieving a list of the actions
    start = time.time()
    plan    = Plan(domainFile, problemFile, plannerType, algorithm)
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