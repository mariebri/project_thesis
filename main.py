from planner import *
from plan_executor import *


def mainPlanner():
    plan    = computePlan(planner="temporal")
    executePlan(plan)



if __name__ == '__main__':
    # main()
    mainPlanner()