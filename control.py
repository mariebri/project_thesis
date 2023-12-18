import casadi as ca
import numpy as np

from world import World
from revolt import ReVolt
from utils import *

class Control:
    def __init__(self, h, vessel: ReVolt, world: World):
        self.h      = h
        self.vessel = vessel
        self.world  = world

        self.eint       = np.zeros((3,1))
        self.lookahead  = 100
        self.roaTransit = 16
        self.roaDock    = 5

        self.f          = np.zeros((3,1))
        self.a          = np.zeros((3,1))

    def inProximity(self, wp, transit=True):
        """
        Goal: Return True when the ship is within the circle of
        acceptance corresponding to the desired waypoint
        """
        if transit:
            roa = self.roaTransit
        else:
            roa = self.roaDock
        
        if np.linalg.norm(wp - self.vessel.eta[:2]) <= roa:
            return True
        return False

    def PID(self, eta_d, transit=True):
        if transit:
            nu_d = np.array([self.vessel.vMax,0,0])
        else:
            nu_d = np.array([0,0,0])
        eta, nu = self.vessel.eta, self.vessel.nu
        rotMat  = self.vessel.getJ(psi=eta[2])

        Kp      = np.diag([100, 100, 200])
        Kd      = np.diag([1000, 1000, 1500])
        Ki      = np.diag([10, 10, 20])

        eta_tilde       = eta - eta_d
        eta_tilde[2]    = ssa(eta_tilde[2])
        eta_tilde_dot   = rotMat @ (nu - nu_d)
        eta_tilde       = eta_tilde[:,np.newaxis]
        eta_tilde_dot   = eta_tilde_dot[:,np.newaxis]

        int_term        = Ki @ self.eint
        for i, force in enumerate(int_term[:, 0]):
            int_term[i,0] = saturate(force, self.vessel.T_min[i], self.vessel.T_max[i])

        tau = - rotMat.T @ (Kp @ eta_tilde + Kd @ eta_tilde_dot + int_term)
        return tau, eta_tilde
    
    def thrustAllocation(self, tau, unconstrained=False):
        """
        Goal: Return u = [u1, u2, u3], a = [a1, a2, a3]

        Unconstrained: u_e = inv(K_e) @ T_pseudoinv @ tau
        where u_e = [u1x, u1y, u2x, u2y, u3x, u3y]

        Constrained:    J = min {tau - T}
        subject to      tau - T(a)F = 0,    |Δf| <= |Δf_max|,   |Δa| <= |Δa_max|
        """

        if unconstrained:
            Te, Ke      = self.vessel.T_e, self.vessel.K_e
            T_pseudoinv = Te.T @ np.linalg.inv(Te @ Te.T)
            u_e         = np.linalg.inv(Ke) @ T_pseudoinv @ tau
            f_e         = Ke @ u_e

            f1  = np.sqrt(f_e[0]**2 + f_e[1]**2)
            f2  = np.sqrt(f_e[2]**2 + f_e[3]**2)
            f3  = np.sqrt(f_e[4]**2 + f_e[5]**2)
            a1  = np.arctan2(u_e[1], u_e[0])
            a2  = np.arctan2(u_e[3], u_e[2])
            a3  = np.arctan2(u_e[5], u_e[4])
            f   = np.array([f1, f2, f3])
            a   = np.array([a1, a2, a3])
            return f, a

        else:
            fmin, fmax  = self.vessel.T_min, self.vessel.T_max
            amin, amax  = [0, 0, -270 * ca.pi/180], [ca.inf, ca.inf, 270 * ca.pi/180]

            f1, f2, f3  = ca.SX.sym('f1'), ca.SX.sym('f2'), ca.SX.sym('f3')
            a1, a2, a3  = ca.SX.sym('a1'), ca.SX.sym('a2'), ca.SX.sym('a3')

            f           = ca.vertcat(f1, f2, f3)
            a           = ca.vertcat(a1, a2, a3)

            x           = ca.vertcat(     f1,      f2,      f3,      a1,      a2,      a3)
            x0          = ca.vertcat(      0,       0,       0,       0,       0,       0)
            lbx         = ca.vertcat(fmin[0], fmin[1], fmin[2], amin[0], amin[1], amin[2])
            ubx         = ca.vertcat(fmax[0], fmax[1], fmax[2], amax[0], amax[1], amax[2])

            func        = tau - self.vessel.getTau_ca(f, a) 
            g           = ca.vertcat(func[0], func[1], func[2], self.f[0]-f1, self.f[1]-f2, \
                                     self.f[2]-f3, self.a[0]-a1, self.a[1]-a2, self.a[2]-a3)
            lbg         = ca.vertcat(-0.1, -0.1, -0.1, -10, -10, -4, -ca.pi/6, -ca.pi/6, -ca.pi/36)
            ubg         = ca.vertcat( 0.1,  0.1,  0.1,  10,  10,  4,  ca.pi/6,  ca.pi/6,  ca.pi/36)

            J           = func[0] + func[1] + func[2]
            nlp         = {'x': x, 'f': J, 'g': g}

            solver      = ca.nlpsol('solver', 'ipopt', nlp, {'ipopt.print_level': 0, 'print_time': 0, 'ipopt.sb': 'yes', 'ipopt.max_cpu_time': 0.025})
            sol         = solver(x0=x0, lbx=lbx, ubx=ubx, lbg=lbg, ubg=ubg)

            x_sol       = sol['x'].full()
            f_sol       = np.array([x_sol[0], x_sol[1], x_sol[2]])
            a_sol       = np.array([x_sol[3], x_sol[4], x_sol[5]])
            return f_sol, a_sol

    def getOptimalEta(self, portFrom, portTo, step=5):
        path        = self.world.findPath(portFrom, portTo)
        path.insert(0, portFrom)
        eta0        = self.vessel.eta

        for i in range(len(path)-1):
            eta_des, _      = self.world.getTransitInfo(path[i], path[i+1])
            eta             = dubinsPath(eta_start=eta0, eta_end=eta_des, step=step)

            if 'eta_opt' in locals():
                eta_opt     = np.concatenate((eta_opt, eta), axis=1)
                eta_toArea.append(path[i+1])
                [eta_toArea.append('') for i in range(eta.shape[1]-1)]
            else:
                eta_opt     = eta
                eta_toArea  = ['' for i in range(eta.shape[1])]
                eta_toArea[0] = path[i+1]
            eta0 = eta_opt[:,-1]

        return eta_opt, eta_toArea
    
    def LOSguidance(self, wp1, wp2):
        x1, y1      = wp1[0], wp1[1]
        x2, y2      = wp2[0], wp2[1]

        pi_p        = np.arctan2(y2-y1, x2-x1)
        rotMat      = np.array([[np.cos(pi_p), -np.sin(pi_p)], [np.sin(pi_p), np.cos(pi_p)]])
        track_err   = rotMat.T @ (self.vessel.eta[:2] - wp1)
        y_e         = track_err[1]

        Kp          = 1/self.lookahead
        chi_d       = ssa(pi_p - np.arctan(Kp * y_e))
        return chi_d, track_err
    
    def headingAutopilot(self, psi_d, wp, transit=True):
        """
        Goal: Steer the vessel in direction of desired heading.

        Steps:  1. Find feedback tau through PID controller
                2. Find thrust input from this tau
                3. Apply thrust input to the vessel

        Returns: eta, nu, tau, f for simulation purposes
        """
        eta_d           = np.array([wp[0], wp[1], psi_d])
        tau, eta_tilde  = self.PID(eta_d, transit)
        self.eint      += self.h*eta_tilde

        self.f, self.a  = self.thrustAllocation(tau)

        eta, nu         = self.vessel.step(self.h, self.f, self.a)
        return eta, nu, self.f
    