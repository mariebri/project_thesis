import numpy as np
import matplotlib.pyplot as plt

from control import Control
from revolt import ReVolt
from utils import *
from world import World

if __name__ == '__main__':
    h           = 0.4
    time        = 0

    world           = World()
    vessel          = ReVolt(x=np.concatenate((world.portA, np.zeros(3))))
    control         = Control(vessel, world)

    eta_d = control.getDubins('A-port', 'C-port')

    world.plot(showInd=True)

    for i in range(eta_d.shape[1]-1):
        pt1     = eta_d[:2,i]
        pt2     = eta_d[:2,i+1]

        # Compute cross-track and along-track error
        pi_p        = np.arctan2(pt2[1]-pt1[1], pt2[0]-pt1[0])
        R           = np.array([[np.cos(pi_p), -np.sin(pi_p)], [np.sin(pi_p), np.cos(pi_p)]])
        track_err   = R.T @ (vessel.eta[:2] - pt1)
        x_e, y_e    = track_err[0], track_err[1]

        # LOS guidance law
        lookahead   = 10
        Kp          = 1/lookahead
        chi_d       = pi_p - np.arctan(Kp * y_e)

        # Course autopilot
        ...


    """
    for i in range(eta_d.shape[1]):
        eta_des = eta_d[:,i]
        steps   = control.getToEta(eta_des, h)
        time   += steps*h

        vessel.plot(eta_des, color='yellow')
        vessel.plot()
        plt.pause(0.001)

    print(time)
    plt.plot(eta_d[0,:], eta_d[1,:], color='green')
    plt.show()
    """