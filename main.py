import argparse
import math
import matplotlib.pyplot as plt

from control import Control
from revolt import ReVolt
from planner import *
from plan_executor import PlanExecutor
from utils import *
from world import World

### Global parameters
plannerType = PlannerType.TEMPORAL
algorithm   = "stp-3"
scenario    = 1

h           = 0.3
N           = 50000

world       = World()
world.plot(showInd=False)


def main(replan, battery, eta0):
    plan    = Planner(plannerType, algorithm, replan, battery, scenario)
    print("\n\nComputation time: ", plan.compTime)
    plan.printPlan()

    # Initialize vessel
    if np.linalg.norm(eta0 - np.zeros(3)) == 0:
        port0   = plan.getStartPos()
        print('Start pos: %s' % port0)
        eta0    = world.getPort(port0)
    x0          = np.concatenate((eta0, np.zeros(3)))
    vessel      = ReVolt(x=x0)
    control     = Control(h, vessel, world)

    # Executing the plan
    planExe = PlanExecutor(plan, control, N)
    planExe.executePlan()

    print('Executing finished ...')
    print('n: %s \nN: %s' % (planExe.n, planExe.N))
    print('Total time: %s' % planExe.time)

    eta_sim = planExe.eta_sim[:, :planExe.n]
    nu_sim  = planExe.nu_sim[:, :planExe.n]
    tau_sim = planExe.tau_sim[:, :planExe.n]

    time_range = np.arange(start=0, stop=planExe.time-h, step=h)

    plt.figure()
    plt.plot(time_range, tau_sim[2,:])
    plt.show()
    


if __name__ == '__main__':
    
    replan  = False
    battery = 100
    eta0    = np.zeros(3)

    # Argument parser
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-r", "--replan", help="1/0")
    argParser.add_argument("-b", "--battery", help="[0, 100] %")
    argParser.add_argument("-x", "--xpos", help="x-position")
    argParser.add_argument("-y", "--ypos", help="y-position")
    argParser.add_argument("-p", "--psi", help="heading angle")

    args    = argParser.parse_args()
    if args.replan == "1":
        replan = True
    if args.battery != None:
        battery = int(args.battery)
    if args.xpos != None:
        x = float(args.xpos)
    if args.ypos != None:
        y = float(args.ypos)
    if args.psi != None:
        p = float(args.psi)
        eta0 = np.array([x, y, p])

    main(replan, battery, eta0)