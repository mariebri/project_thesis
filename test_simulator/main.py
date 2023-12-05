import numpy as np
import matplotlib.pyplot as plt

from control import Control
from revolt import ReVolt
from functions import *
from world import World

if __name__ == '__main__':
    h           = 0.1
    time        = 0

    world           = World()
    vessel          = ReVolt(x=np.concatenate((world.portA, np.zeros(3))))
    control         = Control(vessel, world)

    eta_d = control.transitDubins('A', 'B')

    world.plot(showInd=True)
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