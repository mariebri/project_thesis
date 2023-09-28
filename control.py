import numpy as np
from vessel import Vessel
#import casadi as cd

def speedController(vessel: Vessel, eta_d):
    delta_x = eta_d[0] - vessel.eta[0]
    delta_y = eta_d[1] - vessel.eta[1]
    alpha   = np.arctan2(delta_y, delta_x)

    dist = np.linalg.norm(vessel.eta - eta_d)
    if dist > 500:
        f1, f2, f3 = vessel.Tmax_azimuth, vessel.Tmax_azimuth, vessel.Tmax_tunnel
    else:
        f1, f2 = vessel.Tmax_azimuth*dist/500, vessel.Tmax_azimuth*dist/500
        f3 = vessel.Tmax_tunnel *dist/500
    
    u_e = np.array([f1*np.cos(alpha), f1*np.sin(alpha), f2*np.cos(alpha), f2*np.sin(alpha), f3])
    return u_e

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

"""
def controlAllocationNLP(vessel: Vessel, eta_d, alpha, f):
    
    # Decision variables
    eta = cd.SX.sym("n", 3)
    nu  = cd.SX.sym("v", 3)
    f   = cd.SX.sym("f", 3)
    a   = cd.SX.sym("a", 2)
    x   = cd.vertcat(eta, nu, f, a)

    # Parameters
    p       = 10
    eps     = 0.001
    W       = np.eye(3)
    T       = vessel.getT(alpha)
    eta_dot = vessel.J @ vessel.nu
    nu_dot  = np.linalg.solve(vessel.M, -vessel.D @ vessel.nu + T @ f)


    # Objective function
    f = cd.fabs(eta-eta_d) + cd.fabs(nu) + cd.fabs(f) + p/(eps + np.linalg.det(T@np.linalg.inv(W)@T.T))

    # Nonlinear constraints
    g = cd.vertcat(( \
        eta_dot - vessel.J @ nu,
        vessel.M @ nu_dot + vessel.D @ nu - T @ f
    ))

    # Nonlinear bounds
    lbg = [0, 0, 0, 0, 0, 0]
    ubg = [0, 0, 0, 0, 0, 0]

    # Input bounds for optimization variables
    lbx = [-cd.inf, -cd.inf, -np.pi, -cd.inf, -cd.inf, -cd.inf, -cd.inf, -cd.inf, -cd.inf, -vessel.alphamax, -vessel.alphamax]
    ubx = [cd.inf, cd.inf, np.pi, cd.inf, cd.inf, cd.inf, cd.inf, cd.inf, cd.inf, vessel.alphamax, vessel.alphamax]

    # Initial guess for decision variables
    eta0    = [0, 0, 0]
    nu0     = [0, 0, 0]
    f0      = [0, 0, 0]
    a0      = [0, 0]
    x0      = np.concatenate((eta0, nu0, f0, a0))

    # Create NLP solver
    nlp    = cd.SXFunction(cd.nlpIn(x=x), cd.nlpOut(f=f, g=g))
    solver = cd.NlpSolver("ipopt", nlp)
    solver.init()

    # Pass bounds and initial values
    solver.setInput( x0, "x0")
    solver.setInput(lbx, "lbx")
    solver.setInput(ubx, "ubx")
    solver.setInput(lbg, "lbg")
    solver.setInput(ubg, "ubg")

    solver.evaluate()
"""