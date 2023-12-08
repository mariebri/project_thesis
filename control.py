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
        self.lookahead  = 10
        self.roa        = 8
    
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
        path    = self.world.findPath(portFrom, portTo)
        path.insert(0, portFrom)
        eta0    = self.vessel.eta

        for i in range(len(path)-1):
            eta_des, _  = self.world.getTransitInfo(path[i], path[i+1])
            eta         = dubinsPath(eta_start=eta0, eta_end=eta_des, step=step)

            if 'eta_opt' in locals():
                eta_opt = np.concatenate((eta_opt, eta), axis=1)
            else:
                eta_opt = eta
            eta0 = eta_opt[:,-1]

        return eta_opt
    
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
