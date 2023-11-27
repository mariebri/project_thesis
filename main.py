import sys
from planner import *
from utils import *

def main(replan):
    # Specify the planner type, domain and problem files, and the algorithm
    plannerType = PlannerType.TEMPORAL
    algorithm   = "stp-3"

    # Computing a plan, retrieving a list of the actions
    plan    = Planner(plannerType, algorithm, replan)
    print("\n\nComputation time: ", plan.compTime)
    plan.printPlan()
    plan.executePlan()


if __name__ == '__main__':
    
    replan = False
    if len(sys.argv) == 2:
        if sys.argv[1].lower() == "true":
            replan = True

    main(replan)