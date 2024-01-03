import math
import matplotlib.pyplot as plt

from controller import Controller
from revolt import ReVolt
from planner import *
from plan_executor import PlanExecutor
from utils import *
from world import World

### Global parameters
plannerType = PlannerType.TEMPORAL
algorithm   = "stp-3"
scenario    = 2

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
    controller = Controller(h, vessel, world)

    # Executing the plan
    planExe = PlanExecutor(plan, controller, N)
    planExe.simulation()

    print('Executing finished ...')
    print('Steps n: \t%s \nTotal time: \t%s' % (planExe.n, planExe.time))


    # Simulation parameters
    eta_sim     = planExe.eta_sim[:, :planExe.n]
    nu_sim      = planExe.nu_sim[:, :planExe.n]
    f_sim       = planExe.f_sim[:, :planExe.n]
    etad_sim    = planExe.etad_sim[:, :planExe.n]
    track_err   = planExe.track_err[:, :planExe.n]

    time_range  = np.arange(start=0, stop=planExe.time-h, step=h)
    U_tot       = [(nu_sim[0,i] + nu_sim[1,i]) for i in range(len(time_range))]

    # Plotting
    plt.figure()
    plt.plot(time_range, nu_sim[0,:len(time_range)], label="Surge speed u")
    plt.plot(time_range, nu_sim[1,:len(time_range)], label="Sway speed v")
    plt.plot(time_range, U_tot[:len(time_range)], label="Total speed U")
    plt.title('Vessel speed')
    plt.ylabel('Speed [m/s]'), plt.xlabel('Time [sec]')
    plt.grid(), plt.legend()

    plt.figure()
    plt.plot(time_range, f_sim[0,:len(time_range)], label="F1 [N]")
    plt.plot(time_range, f_sim[1,:len(time_range)], label="F2 [N]")
    plt.plot(time_range, f_sim[2,:len(time_range)], label="F3 [Nm]")
    plt.title('Control forces')
    plt.ylabel('Force [N(m)]'), plt.xlabel('Time [sec]')
    plt.grid(), plt.legend()

    plt.figure()
    plt.plot(time_range, track_err[0, :len(time_range)], label="Along-track error x_e")
    plt.plot(time_range, track_err[1, :len(time_range)], label="Cross-track error y_e")
    plt.title('Along-track and Cross-track errors')
    plt.ylabel('Error [m]'), plt.xlabel('Time [sec]')
    plt.grid(), plt.legend()

    plt.figure()
    plt.plot(time_range, eta_sim[2, :len(time_range)], label="Simulated heading")
    plt.plot(time_range, etad_sim[2, :len(time_range)], label="Desired heading")
    plt.title("Desired vs Actual heading")
    plt.ylabel('Heading [rad]'), plt.xlabel('Time [sec]')
    plt.grid(), plt.legend()

    plt.figure()
    world.plot()
    for i in range(len(time_range)):
        if i % math.floor(10/controller.h) == 0:
            if i >= planExe.nReplan:
                color = 'red'
            else:
                color = 'green'
            if np.linalg.norm(eta_sim[:,i]) >= 1000:
                vessel.plot(eta_sim[:,i], color=color)
        #vessel.plot(etad_sim[:,i], color="yellow")
    
    
    etad = np.zeros((2,len(time_range)))
    j = 0
    for i in range(etad_sim.shape[1]):
        if etad_sim[0,i] >= 1:
            etad[:,j] = etad_sim[:2,i]
            j += 1
        #plt.plot(etad[0,:j], etad[1,:j], color="yellow")
    
    plt.show()
    


if __name__ == '__main__':

    main()