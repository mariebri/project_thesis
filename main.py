import numpy as np
from vessel import Vessel
from plotting import plot


# Simulation parameters
sampleTime  = 0.02          # sample time [seconds]
N           = 10000         # number of samples

# Initial states
x = [100, 100, np.pi/2, 1, 0, 0]
u = [5, 5, 5, -np.pi, np.pi/2]

vehicle = Vessel(x, u)


def main():
    simData = np.zeros((6, N))
    for i in range(N):
        x = vehicle.dynamics(u, sampleTime)
        simData[:,i] = x

    waypoints = np.array([[100,200], [100,200]])
    trajectory = np.array([simData[0,:], simData[1,:]])
    plot(waypoints, trajectory)


main()