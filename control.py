import numpy as np
#import casadi as ca
from vessel import Vessel

def PID(vessel: Vessel, eta_d, nu_d, eta_tilde_int):
    
    Kp = np.diag([1000, 1000, 10000])
    Kd = np.diag([1000, 1000, 15000])
    Ki = np.diag([10, 10, 20])

    eta_tilde = vessel.eta - eta_d
    eta_tilde_dot = vessel.J @ (vessel.nu - nu_d)

    tau = - vessel.J.T @ (Kp @ eta_tilde + Kd @ eta_tilde_dot + Ki @ eta_tilde_int)
    return tau, eta_tilde

def controlAllocation(vessel: Vessel, tau):
    T_e = vessel.getT_e()
    u_e = np.reshape(T_e.T @ np.linalg.inv(T_e @ T_e.T) @ tau, 5)    # u_e = [u1x, u1y, u2x, u2y, u3]
    return u_e