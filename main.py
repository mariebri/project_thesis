import argparse
import matplotlib.pyplot as plt

from control import Control
from revolt import ReVolt
from planner import *
from plan_executor import PlanExecutor
from utils import *
from world import World

plannerType = PlannerType.TEMPORAL
algorithm   = "stp-3"
scenario    = 1


def planning(replan, battery, control):
    plan    = Planner(plannerType, algorithm, replan, battery, scenario)
    print("\n\nComputation time: ", plan.compTime)
    plan.printPlan()

    # Executing the plan
    planExe = PlanExecutor(plan, control)
    planExe.executePlan()
    plt.show()


def main(replan, battery):
    # Initializing environment
    h       = 0.4
    world   = World()
    world.plot(showInd=True)

    x0      = np.concatenate((world.portA, np.zeros(3)))
    vessel  = ReVolt(x=x0)
    control = Control(vessel, world)

    # Computing a plan, retrieving a list of the actions
    planning(replan, battery, control)
    


if __name__ == '__main__':
    
    replan  = False
    battery = 100

    # Argument parser
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-r", "--replan", help="True/False")
    argParser.add_argument("-b", "--battery", help="[0, 100] %")

    args    = argParser.parse_args()
    if args.replan == "True":
        replan = True
    if args.battery != None:
        battery = int(args.battery)

    main(replan, battery)