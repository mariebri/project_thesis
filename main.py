import numpy as np
from vessel import Vessel
from plotting import plot
from control import *

def main():

    # Simulation parameters
    sampleTime  = 0.01          # sample time [seconds]
    N           = 100000         # number of samples

    # Initial states
    x = np.array([100, 100, np.pi/8, 0, 0, 0])
    u_e = np.array([0, 0, 0, 0, 0])
    vessel = Vessel(x, u_e)

    # Desired state
    eta_d = np.array([200, 250, np.pi/2])
    nu_d = np.zeros(3)
    eta_tilde_int = np.zeros(3)

    # Simulation loop
    simData = np.zeros((6, N))
    for i in range(N):

        """ Controller
        tau, eta_tilde = PID(vessel, eta_d, nu_d, eta_tilde_int)
        eta_tilde_int += sampleTime*eta_tilde
        u_e = controlAllocation(vessel, tau)
        """
        u_e = speedController(vessel, eta_d)

        x = vessel.dynamics(u_e, sampleTime)
        simData[:,i] = x

    # Plotting
    waypoints = np.array([[100,200], [100,250]])
    trajectory = np.array([simData[0,:], simData[1,:]])
    plot(waypoints, trajectory)

    # Print final results
    print('Final position: ', simData[:3,-1])
    print('Desired final position: ', eta_d)


main()