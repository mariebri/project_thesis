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
    vessel          = ReVolt(x=np.concatenate((world.portA, np.zeros(3))))
    control         = Control(vessel, world)

    x_opt, u_opt = control.transit('A', 'B')

    world.plot(True)
    for i in range(x_opt.shape[1]):
        #x, u = control.getToEtaD(i) # <-- Doesn't work as of right now :)
        vessel.plot()
        vessel.plot(eta=x_opt[:3, i])
        plt.pause(0.001)

    plt.plot(x_opt[0,:], x_opt[1,:], color='green')
    print(x_opt[0,-1], x_opt[1,-1])

    plt.show()
