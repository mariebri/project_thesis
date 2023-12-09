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
scenario    = 3

h           = 0.3
N           = 50000

world       = World()


def main():
    plan    = Planner(plannerType, algorithm, scenario)
    print("\n\nComputation time: ", plan.compTime)
    plan.printPlan()

    # Initialize vessel
    port0   = plan.getStartPos()
    eta0    = world.getPort(port0)
    x0      = np.concatenate((eta0, np.zeros(3)))
    vessel  = ReVolt(x=x0)
    control = Control(h, vessel, world)

    # Executing the plan
    planExe = PlanExecutor(plan, control, N)
    #planExe.executePlan()
    planExe.simulationLoop()

    print('Executing finished ...')
    print('n: %s \nN: %s' % (planExe.n, planExe.N))
    print('Total time: %s' % planExe.time)

    eta_sim = planExe.eta_sim[:, :planExe.n]
    nu_sim  = planExe.nu_sim[:, :planExe.n]
    tau_sim = planExe.tau_sim[:, :planExe.n]
    U_sim   = planExe.U_sim[:planExe.n]

    time_range = np.arange(start=0, stop=planExe.time-h, step=h)

    plt.figure()
    plt.plot(time_range, tau_sim[2,:len(time_range)])

    plt.figure()
    plt.plot(time_range, U_sim[:len(time_range)])

    plt.figure()
    world.plot()
    for i in range(len(time_range)):
        if i % math.floor(10/control.h) == 0:
            vessel.plot(eta_sim[:,i])
    plt.show()
    


if __name__ == '__main__':

    main()