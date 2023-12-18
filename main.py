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
N           = 40000

world       = World()


def main():
    plan    = Planner(plannerType, algorithm, scenario)

    # Initialize vessel
    port0   = plan.getStartPos()
    eta0    = world.getPort(port0)
    x0      = np.concatenate((eta0, np.zeros(3)))
    vessel  = ReVolt(x=x0)
    control = Control(h, vessel, world)

    # Executing the plan
    planExe = PlanExecutor(plan, control, N)
    planExe.simulation()

    print('Executing finished ...')
    print('Steps n: \t%s \nTotal time: \t%s' % (planExe.n, planExe.time))


    # Simulation parameters
    eta_sim     = planExe.eta_sim[:, :planExe.n]
    nu_sim      = planExe.nu_sim[:, :planExe.n]
    f_sim       = planExe.f_sim[:, :planExe.n]
    etad_sim    = planExe.etad_sim[:, :planExe.n]
    track_err   = planExe.track_err[:, :planExe.n]

    time_range = np.arange(start=0, stop=planExe.time-h, step=h)

    # Plotting
    plt.figure()
    plt.plot(time_range, nu_sim[0,:len(time_range)], label="u")
    plt.plot(time_range, nu_sim[1,:len(time_range)], label="v")
    plt.title('Surge and Sway speed')
    plt.ylabel('Spped [m/s]'), plt.xlabel('Time [sec]')
    plt.grid(), plt.legend()

    plt.figure()
    plt.plot(time_range, f_sim[0,:len(time_range)], label="F1 [N]")
    plt.plot(time_range, f_sim[1,:len(time_range)], label="F2 [N]")
    plt.plot(time_range, f_sim[2,:len(time_range)], label="F3 [Nm]")
    plt.title('Control forces')
    plt.ylabel('Force [N(m)]'), plt.xlabel('Time [sec]')
    plt.grid(), plt.legend()

    plt.figure()
    plt.plot(time_range, track_err[0, :len(time_range)], label="x_e")
    plt.plot(time_range, track_err[1, :len(time_range)], label="y_e")
    plt.title('Cross- and Along-track errors')
    plt.ylabel('Error [rad]'), plt.xlabel('Time [sec]')
    plt.grid(), plt.legend()

    plt.figure()
    world.plot(showInd=True)
    for i in range(len(time_range)):
        if i % math.floor(10/control.h) == 0:
            if i >= planExe.nReplan:
                color = 'red'
            else:
                color = 'blue'
            vessel.plot(eta_sim[:,i], color=color)
            vessel.plot(etad_sim[:,i], color="yellow")
    plt.show()
    


if __name__ == '__main__':

    main()