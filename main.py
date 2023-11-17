from planner import *
from plan_executor import PlanExecutor
from vessel_state import VesselState


def mainPlanner():
    # Specify the planner type, domain and problem files, and the algorithm
    plannerType = PlannerType.TEMPORAL
    domainFile  = "/home/marie/project_thesis/Planning/temporal_domain.pddl"
    problemFile = "/home/marie/project_thesis/Planning/replan_problem.pddl"
    algorithm   = "stp-2"

    #plannerType = PlannerType.GRAPHPLAN
    #domainFile  = "/home/marie/project_thesis/Planning/simple_domain.pddl"
    #problemFile = "/home/marie/project_thesis/Planning/replan_problem.pddl"


    # Computing a plan, retrieving a list of the actions
    plan    = Plan(domainFile, problemFile, plannerType, algorithm)
    actions = plan.getActions()
    init, goal = plan.getPredicates()


    # Declaring a vessel and a plan executor
    vessel  = VesselState(plan, remainingActions=actions, initPred=init, goalPred=goal)
    planExe = PlanExecutor(vessel, plannerType)

    # Executing the plan
    planExe.executePlan()



if __name__ == '__main__':
    mainPlanner()