import sys
import matplotlib.pyplot as plt

from control import Control
from revolt import ReVolt
from planner import *
from plan_executor import PlanExecutor
from utils import *
from world import World

def main(replan, fuelLevel):
    # Specify the planner type, domain and problem files, and the algorithm
    plannerType = PlannerType.TEMPORAL
    algorithm   = "stp-3"
    scenario    = 1

    # Initializing environment
    h       = 0.4
    world   = World()
    world.plot(showInd=True)

    x0      = np.concatenate((world.portA, np.zeros(3)))
    vessel  = ReVolt(x=x0)
    control = Control(vessel, world)

    # Computing a plan, retrieving a list of the actions
    plan    = Planner(plannerType, algorithm, replan, fuelLevel, scenario)
    print("\n\nComputation time: ", plan.compTime)
    plan.printPlan()

    # Executing the plan
    planExe = PlanExecutor(plan, control)
    planExe.executePlan()
    plt.show()


if __name__ == '__main__':
    
    replan      = False
    fuelLevel   = 100

    if len(sys.argv) == 3:
        if sys.argv[1].lower() == "true":
            replan = True
            fuelLevel = int(sys.argv[2])

    main(replan, fuelLevel)