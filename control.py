import numpy as np
import matplotlib.pyplot as plt

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
        self.roa        = 8

        self.T          = 2.4457
        self.K          = -0.1371
        self.zeta       = 1
        self.wn         = 1

        self.eintFossen = 0
        self.psi_d      = 0
        self.r_d        = 0
        self.a_d        = 0

    def inProximity(self, wp):
        """
        Goal: Return True when the ship is within the circle of
        acceptance corresponding to the desired waypoint
        """
        if np.linalg.norm(wp - self.vessel.eta[:2]) <= self.roa:
            return True
        return False

    def PID(self, eta_d, nu_d=np.array([0,0,0])):
        eta, nu = self.vessel.eta, self.vessel.nu
        rotMat  = self.vessel.getJ(psi=eta[2])

        Kp      = np.diag([1000, 1000, 10000])
        Kd      = np.diag([1000, 1000, 15000])
        Ki      = np.diag([10, 10, 20])

        eta_tilde       = eta - eta_d
        eta_tilde[2]    = ssa(eta_tilde[2])
        eta_tilde_dot   = rotMat @ (nu - nu_d)
        eta_tilde       = eta_tilde[:,np.newaxis]
        eta_tilde_dot   = eta_tilde_dot[:,np.newaxis]

        int_term        = Ki @ self.eint
        force_sat       = self.vessel.T_max
        for i, force in enumerate(int_term[:, 0]):
            if abs(force) > force_sat[i]:
                saturated_force = np.sign(force) * force_sat[i]
                int_term[i, 0] = saturated_force

        tau = - rotMat.T @ (Kp @ eta_tilde + Kd @ eta_tilde_dot + int_term)
        return tau, eta_tilde
    
    def thrustAllocation(self, tau, unconstrained=True):
        """
        Goal: Return u = [u1, u2, u3], a = [a1, a2, a3]

        Unconstrained: u_e = inv(K_e) @ T_pseudoinv @ tau
        where u_e = [u1x, u1y, u2x, u2y, u3x, u3y]
        """

        if unconstrained:
            Te, Ke      = self.vessel.T_e, self.vessel.K_e
            T_pseudoinv = Te.T @ np.linalg.inv(Te @ Te.T)
            u_e         = np.linalg.inv(Ke) @ T_pseudoinv @ tau
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
        return chi_d
    
    def headingAutopilot(self, psi_d, wp):
        eta_d           = np.array([wp[0], wp[1], psi_d])
        tau, eta_tilde  = self.PID(eta_d)
        self.eint      += self.h*eta_tilde
        u, a            = self.thrustAllocation(tau)
        eta, nu         = self.vessel.step(self.h, u, a)
        return eta, nu, tau
    
    def refModel3(self, xd, vd, ad, r):
        jd = self.wn**3*(r-xd) - (2*self.zeta+1)*self.wn**2*vd - (2*self.zeta+1)*self.wn*ad

        xd += self.h * vd
        vd += self.h * ad
        ad += self.h * jd

        vMax = self.vessel.vMax
        vd = saturate(vd, -vMax, vMax)
        return xd, vd, ad
    
    def PIDpolePlacement(self, eint, ex, ev, xd, vd, ad, m, d, k, r):
        Kp = m * self.wn**2 - k
        Kd = m*2*self.zeta*self.wn - d
        Ki = (self.wn / 10) * Kp

        u = -Kp*ex - Kd*ev - Ki*eint
        eint += self.h*ex

        [xd, vd, ad] = self.refModel3(xd, vd, ad, r)
        return u, eint, xd, vd, ad

    def headingAutopilotFossen(self):
        psi, r  = self.vessel.eta[2], self.vessel.nu[2]
        epsi    = psi - self.psi_d
        er      = r - self.r_d

        m       = self.T / self.K
        d       = 1 / self.K
        k       = 0

        [delta, self.eintFossen, self.psi_d, self.r_d, self.a_d] = \
            self.PIDpolePlacement(self.eintFossen, epsi, er, self.psi_d, \
                                  self.r_d, self.a_d, m, d, k, r)
        
        u_control = np.array([delta], float)

        return u_control