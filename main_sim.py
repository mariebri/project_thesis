import numpy as np
import matplotlib.pyplot as plt

from control import Control
from revolt import ReVolt
from utils import *
from world import World

if __name__ == '__main__':
    h       = 0.4
    time    = 0
    eint    = np.zeros((3,1))
    roa     = 8
    N       = 20000

    world           = World()
    vessel          = ReVolt(x=np.concatenate((world.portB, np.zeros(3))))
    control         = Control(h, vessel, world)

    # Simulation parameters
    eta_sim     = np.zeros((3,N))
    nu_sim      = np.zeros((3,N))
    tau_sim     = np.zeros((3,N))


    world.plot(showInd=True)
    eta_d = control.getOptimalEta('B-port', 'C-port')

    i   = 0
    wp1 = eta_d[:2,i]
    wp2 = eta_d[:2,i+1]
    for n in range(N):
        if inProximity(wp2, vessel.eta[:2], roa):
            i  += 1
            wp1 = eta_d[:2,i]
            wp2 = eta_d[:2,i+1]

            if i == eta_d.shape[1]-3:
                roa = 3
            if i == eta_d.shape[1]-2:
                N = n+1
                break

        # LOS Guidance to find desired course
        chi_d       = control.LOSguidance(wp1, wp2)

        # Heading autopilot
        psi_d               = chi_d - vessel.getCrabAngle()
        eta, nu, tau, eint  = control.headingAutopilot(psi_d, wp2, eint)

        # Storing simulation parameters
        eta_sim[:,n]    = eta
        nu_sim[:,n]     = nu
        tau_sim[:,n]    = tau.reshape(3)

        if n % 40 == 0 or n == N-1:
            vessel.plot()
            plt.pause(0.01)
            
    plt.show()