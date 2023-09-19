import numpy as np
from vessel import Vessel
from plotting import plotTrajectory


# Simulation parameters
sampleTime  = 0.02          # sample time [seconds]
N           = 10000         # number of samples

# Initial states
x = [0, 0, np.pi/2, 1, 0, 0]
u = [5, 5, 5, -np.pi, np.pi/2]

vehicle = Vessel(x, u)

# Main loop
def main():
    #[simTime, simData] = simulate(N, sampleTime, vehicle)

    # Plots:
    # plotVehicleStates(simTime, simData, 1)
    # plotControls(simTime, simData, vehicle, 2)
    # plot3D(simData, numDataPoints, FPS, filename, 3)

    # plt.show()
    # plt.close() (?)


    simData = np.zeros((6, N))
    for i in range(N):
        x = vehicle.dynamics(u, sampleTime)
        simData[:,i] = x

    plotTrajectory(simData)


main()