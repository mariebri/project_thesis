import sys
from planner import *
from utils import *

def main(replan, fuelLevel):
    # Specify the planner type, domain and problem files, and the algorithm
    plannerType = PlannerType.TEMPORAL
    algorithm   = "stp-3"

    # Computing a plan, retrieving a list of the actions
    plan    = Planner(plannerType, algorithm, replan, fuelLevel)
    print("\n\nComputation time: ", plan.compTime)
    plan.printPlan()
    plan.executePlan()


if __name__ == '__main__':
    
    replan      = False
    fuelLevel   = 100

    if len(sys.argv) == 3:
        if sys.argv[1].lower() == "true":
            replan = True
            fuelLevel = int(sys.argv[2])

    main(replan, fuelLevel)