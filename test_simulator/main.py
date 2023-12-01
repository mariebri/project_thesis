import revolt
import numpy as np
import matplotlib.pyplot as plt
from control import trajectory
from world import World

if __name__ == '__main__':
    h       = 0.1
    T       = 50
    x       = np.zeros(6)

    vessel          = revolt.ReVolt(x=x)
    world           = World()

    x0              = np.array([world.portA[0], world.portA[1], 0, 0, 0, 0])
    u0              = x0
    x_opt, u_opt    = trajectory(eta_des=np.array([world.portB[0], world.portB[1], 0]), x0=x0, u0=u0, h=h, vessel=vessel, T=T)

    world.plotMap()
    for i in range(int(T/h)):
        #vessel.step(h, u_opt[:, i])
        vessel.plot(eta=x_opt[:3, i+1])
        #plt.pause(0.001)

    plt.plot(x_opt[1,:], x_opt[0,:], color='green')
    plt.show()
