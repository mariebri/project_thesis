import casadi as ca
import numpy as np
import dubins

from enum import Enum
from revolt import ReVolt

PlannerType = Enum('PlannerType', ['TEMPORAL', 'GRAPHPLAN'])
State       = Enum('State', ['DOCKED', 'DOCKING', 'UNDOCKING', 'IN_TRANSIT'])

def getDomainProblemFiles(plannerType: PlannerType, scenario=1, replan=False):
    if plannerType == PlannerType.TEMPORAL:
        domainFile  = "/home/marie/project_thesis/Planning/TEMPORAL/domain.pddl"
        if scenario == 1:
            problemFile = "/home/marie/project_thesis/Planning/TEMPORAL/p1.pddl"
        elif scenario == 2:
            problemFile = "/home/marie/project_thesis/Planning/TEMPORAL/p2.pddl"
        elif scenario == 3:
            problemFile = "/home/marie/project_thesis/Planning/TEMPORAL/p3.pddl"

    elif plannerType == PlannerType.GRAPHPLAN:
        domainFile  = "/home/marie/project_thesis/Planning/CLASSICAL/domain.pddl"
        if scenario == 1:
            problemFile = "/home/marie/project_thesis/Planning/CLASSICAL/p1.pddl"
        elif scenario == 2:
            problemFile = "/home/marie/project_thesis/Planning/CLASSICAL/p2.pddl"
        elif scenario == 3:
            problemFile = "/home/marie/project_thesis/Planning/CLASSICAL/p3.pddl"

    if replan:
        problemFile = "/home/marie/project_thesis/Planning/replan_problem.pddl"

    return domainFile, problemFile

def getPortName(portFrom: str, portTo="", state=State.IN_TRANSIT):
    portFrom    = (portFrom.strip('-port')).upper()
    if portTo != "":
        portTo      = (portTo.strip('port')).upper()
    
    if state == State.DOCKING:
        portTo      = portFrom + "-port"
    elif state == State.UNDOCKING:
        portTo      = portFrom
        portFrom    = portTo + "-port"
    
    return portFrom, portTo

def ssa(angle):
    return ca.fmod(angle + ca.pi, 2*ca.pi) - ca.pi

def trajectory(eta_des, x0, u0, harbor, vessel: ReVolt, T=20, h=2):
    x0 = x0[:,np.newaxis]
    u0 = u0[:,np.newaxis]
    d = 3
    tau_root = np.append(0, ca.collocation_points(d, 'legendre'))
    C = np.zeros((d+1,d+1))
    D = np.zeros(d+1)
    B = np.zeros(d+1)

    # Construct polynomial basis
    for j in range(d+1):
        p = np.poly1d([1])
        for r in range(d+1):
            if r != j:
                p *= np.poly1d([1, -tau_root[r]]) / (tau_root[j]-tau_root[r])
        D[j] = p(1.0)
        pder = np.polyder(p)
        for r in range(d+1):
            C[j,r] = pder(tau_root[r])
        pint = np.polyint(p)
        B[j] = pint(1.0)

    # Symbolic state
    x_pos = ca.SX.sym('x_pos')
    y_pos = ca.SX.sym('y_pos')
    psi   = ca.SX.sym('psi')
    eta   = ca.vertcat(x_pos, y_pos, psi)

    u     = ca.SX.sym('u')
    v     = ca.SX.sym('v')
    r     = ca.SX.sym('r')
    nu    = ca.vertcat(u, v, r)

    x     = ca.vertcat(eta, nu)
    num_var = x.shape[0]

    # Symbolic desired state
    x_pos_d = ca.SX.sym('x_pos_d')
    y_pos_d = ca.SX.sym('y_pos_d')
    psi_d   = ca.SX.sym('psi_d')
    eta_d   = ca.vertcat(x_pos_d, y_pos_d, psi_d)

    u_d     = ca.SX.sym('u_d')
    v_d     = ca.SX.sym('v_d')
    r_d     = ca.SX.sym('r_d')
    nu_d    = ca.vertcat(u_d, v_d, r_d)
    nu_des  = np.array([0,0,0])  # If transit?

    # Symbolic input
    f1x = ca.SX.sym('f1x')
    f1y = ca.SX.sym('f1y')
    f2x = ca.SX.sym('f2x')
    f2y = ca.SX.sym('f2y')
    f3x = ca.SX.sym('f3x')
    f3y = ca.SX.sym('f3y')
    f  = ca.vertcat(f1x, f1y, f2x, f2y, f3x, f3y)

    num_input = f.shape[0]

    # Vessel mode
    f_max = vessel.T_max
    f_min = vessel.T_min

    R = ca.vertcat(ca.horzcat(ca.cos(psi), -ca.sin(psi), 0),
                   ca.horzcat(ca.sin(psi),  ca.cos(psi), 0),
                   ca.horzcat(          0,            0, 1))
    
    eta_dot = R @ nu
    nu_dot  = ca.solve((vessel.M_ca), (-(vessel.getC(nu, casadi=True) + vessel.D_ca) @ nu + vessel.T_ca @ f))
    x_dot   = ca.vertcat(nu_dot, eta_dot)

    # Objective function
    Q_eta   = ca.diag([1e4,   1e4,   1e6])
    Q_nu    = ca.diag([1e2, 1e5, 1e7])
    R_f     = ca.diag([1e-2, 1e-2, 1e-2, 1e-2, 1e-2, 1e-2])

    obj = (eta[:2]-eta_d[:2]).T @ Q_eta[:2, :2] @ (eta[:2]-eta_d[:2]) + ssa(eta[2]-eta_d[2]) * Q_eta[2, 2] * ssa(eta[2]-eta_d[2]) + (nu-nu_d).T @ Q_nu @ (nu-nu_d) + f.T @ R_f @ f
    func = ca.Function('func', [x, eta_d, nu_d, f], [x_dot, obj])

    # Vessel size
    margin = 1.1
    vessel_vm = vessel.vBox
    R_ned = ca.vertcat(ca.horzcat(ca.cos(psi), -ca.sin(psi)),
                       ca.horzcat(ca.sin(psi),  ca.cos(psi)))
    
    # Harbor
    As = harbor['A']
    bs = harbor['b']
    Ax_harbor = As @ ((R_ned @ vessel_vm).T + ca.repmat(ca.horzcat(x_pos, y_pos), 4, 1)).T
    f_harbor = ca.Function('f_harbor', [x], [Ax_harbor])

    # Initialize NLP
    # Empty NLP
    w = [] 
    w0 = []
    lbw = []
    ubw = []
    J = 0
    g =[]
    lbg = []
    ubg = []

    x_hist = []
    u_hist = []

    # Bounds
    lbx = ca.vertcat(-ca.inf, -ca.inf, -ca.inf, -1, -0.5, -0.2)
    ubx = ca.vertcat(ca.inf, ca.inf, ca.inf, 6, 0.5, 0.2)
    lbu = ca.vertcat(f_min[0], f_min[0], f_min[1], f_min[1], f_min[2], f_min[2])
    ubu = ca.vertcat(f_max[0], f_max[0], f_max[1], f_max[1], f_max[2], f_max[2])

    Xk = ca.MX.sym('X0', num_var)
    w.append(Xk)
    lbw.append(x0)
    ubw.append(x0)
    w0.append(x0)
    x_hist.append(Xk)

    epsilon = 1e-3
    eps_model = 1e-3
    slack_const = 50000
    for k in range(int(T/h)):
        if eps_model > 1e-5:
            eps_model /= 10
        slack = ca.vertcat(0, 0, 0, 0, slack_const*eps_model, slack_const*eps_model)

        # New NLP variable for the control
        Uk = ca.MX.sym('U_' + str(k), num_input)
        w.append(Uk)
        lbw.append(lbu)
        ubw.append(ubu)
        w0.append(u0)
        u_hist.append(Uk)

        Xc = []
        for j in range(d):
            Xkj = ca.MX.sym('X_'+str(k)+'_'+str(j), num_var)
            Xc.append(Xkj)
            w.append(Xkj)
            lbw.append(lbx - slack)
            ubw.append(ubx + slack)
            w0.append(x0)

        Xk_end = D[0]*Xk
        for j in range(1,d+1):
            # Expression for the state derivative at the collocation point
            xp = C[0,j]*Xk
            for r in range(d): xp = xp + C[r+1,j]*Xc[r] 

            # Append collocation equations
            fj, qj = func(Xc[j-1], eta_des, nu_des, Uk)
            g.append(h*fj[:5,0] - xp[:5,0])
            g.append(ssa(h*fj[5,0] - xp[5,0]))
            lbg.append([-eps_model, -eps_model, -eps_model, -eps_model, -eps_model ,-eps_model])
            ubg.append([eps_model, eps_model, eps_model, eps_model, eps_model, eps_model])

            # Add contribution to the end state
            Xk_end = Xk_end + D[j]*Xc[j-1]

            # Add contribution to quadrature function
            J = J + B[j]*qj*h

        Xk = ca.MX.sym('X_' + str(k+1), num_var)
        w.append(Xk)
        lbw.append(lbx - slack)
        ubw.append(ubx + slack)
        w0.append(x0)
        x_hist.append(Xk)

        # Add equality constraint
        g.append(Xk_end[:5]-Xk[:5]) 
        g.append(ssa(Xk_end[5]-Xk[5]))
        lbg.append([-epsilon, -epsilon, -epsilon, -epsilon, -epsilon, -epsilon])
        ubg.append([epsilon, epsilon, epsilon, epsilon, epsilon, epsilon])

        # Harbor
        Ax = f_harbor(Xk)
        for i in range(4):
            g.append(Ax[:,i])
            lbg.append([-np.inf for lower_bound in range(bs.shape[0])])
            ubg.append(bs)

    # Concatenate vectors
    w = ca.vertcat(*w)
    g = ca.vertcat(*g)
    x_hist = ca.horzcat(*x_hist)
    u_hist = ca.horzcat(*u_hist)
    w0 = np.concatenate(w0)
    lbw = np.concatenate(lbw)
    ubw = np.concatenate(ubw)
    lbg = np.concatenate(lbg)
    ubg = np.concatenate(ubg)

    prob = {'f': J, 'x': w, 'g': g}
    opt = {'ipopt.print_level': 0, 'print_time': 0, 'ipopt.sb': 'yes'}
    solver = ca.nlpsol('solver', 'ipopt', prob, opt)
    
    sol = solver(x0=w0, lbx=lbw, ubx=ubw, lbg=lbg, ubg=ubg)
    status = solver.stats()
    if status["return_status"] == "Infeasible_Problem_Detected":
        print("Infeasible solution:")
        constraints = sol['g'].full()
        size_g = constraints.shape[0]
        for i in range(size_g):
            g_val = constraints[i,0]
            g_low = lbg[i]
            g_high = ubg[i]
            if g_val < g_low or g_val > g_high:
                print("g", i, ":", g_low, "<", g_val, "<", g_high)

        states = sol['x'].full()
        size_x = states.shape[0]
        for i in range(size_x):
            x_val = states[i,0]
            x_low = lbw[i,0]
            x_high = ubw[i,0]
            if x_val < x_low or x_val > x_high:
                print("x", i, ":", x_low, "<", x_val, "<", x_high)

        print("Searched for infeasibility")

    # Function to get x and u trajectories from w
    trajectories = ca.Function('trajectories', [w], [x_hist, u_hist], ['w'], ['x', 'u'])
    x_opt, u_opt = trajectories(sol['x'])
    x_opt = x_opt.full() # to numpy array
    u_opt = u_opt.full() # to numpy array
    
    return x_opt, u_opt

def thrustAllocation(tau, vessel: ReVolt, unconstrained=True):
    """
    Goal: Return u = [u1, u2, u3], a = [a1, a2, a3]

    Unconstrained: u_e = inv(K_e) @ T_pseudoinv @ tau
    where u_e = [u1x, u1y, u2x, u2y, u3x, u3y]
    """

    if unconstrained:
        Te, Ke      = vessel.T_e, vessel.K_e
        B           = Te @ Ke
        B_pseudoinv = B.T @ np.linalg.inv(B @ B.T)
        #T_pseudoinv = Te.T @ np.linalg.inv(Te @ Te.T)
        #u_e         = np.linalg.inv(Ke) @ T_pseudoinv @ tau
        u_e         = B_pseudoinv @ tau
    else:
        # TODO
        u_e = np.zeros(6)

    u1  = np.sqrt(u_e[0]**2 + u_e[1]**2)
    u2  = np.sqrt(u_e[2]**2 + u_e[3]**2)
    u3  = np.sqrt(u_e[4]**2 + u_e[5]**2)
    a1  = np.arctan2(u_e[1], u_e[0])
    a2  = np.arctan2(u_e[3], u_e[2])
    a3  = np.arctan2(u_e[5], u_e[4])
    u   = np.array([u1, u2, u3])
    a   = np.array([a1, a2, a3])

    return u, a

def PIDcontroller(eta_p, nu_p, eta_tilde_int, vessel: ReVolt):
    eta     = vessel.eta
    nu      = vessel.nu
    J       = vessel.getJ(psi=eta[2])

    Kp      = np.diag([1000, 1000, 10000])
    Kd      = np.diag([1000, 1000, 15000])
    Ki      = np.diag([10, 10, 20])

    eta_tilde       = eta - eta_p
    eta_tilde_dot   = J @ (nu - nu_p)
    eta_tilde       = eta_tilde[:,np.newaxis]
    eta_tilde_dot   = eta_tilde_dot[:,np.newaxis]

    int_term        = Ki @ eta_tilde_int
    force_sat       = vessel.T_max
    for i, force in enumerate(int_term[:, 0]):
        if abs(force) > force_sat[i]:
            saturated_force = np.sign(force) * force_sat[i]
            int_term[i, 0] = saturated_force

    tau_fb = - J.T @ (Kp @ eta_tilde + Kd @ eta_tilde_dot + int_term)
    return tau_fb, eta_tilde

def dubinsPath(eta_start, eta_end, curvature=1.0, step=5):
    path        = dubins.shortest_path(eta_start, eta_end, curvature)
    eta_d, _    = path.sample_many(step)

    # Make eta_d a 3xN matrix
    eta         = np.zeros((3, len(eta_d)))  
    for i in range(len(eta_d)):
        e       = eta_d[i]
        eta[0,i]= e[0]
        eta[1,i]= e[1]
        eta[2,i]= ssa(e[2])
    
    return eta

def inProximity(eta, eta_d):
    if np.linalg.norm(eta - eta_d) <= 0.1:
        return True
    return False