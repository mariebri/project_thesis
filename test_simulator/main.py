import numpy as np
import matplotlib.pyplot as plt

from control import Control
from revolt import ReVolt
from functions import *
from world import World

if __name__ == '__main__':
    h           = 0.1
    ts          = 20
    T_horizon   = 2500

    world           = World()
    vessel          = ReVolt(x=np.concatenate((world.portD, np.zeros(3))))
    control         = Control(vessel, world)

    eta_d = control.transitDubins('D', 'A')

    world.plot(True)
    for i in range(eta_d.shape[1]):
        vessel.plot(eta_d[:,i], color='yellow')
        plt.pause(0.01)

    plt.plot(eta_d[0,:], eta_d[1,:], color='green')
    plt.show()