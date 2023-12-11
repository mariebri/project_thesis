import matplotlib.pyplot as plt
import numpy as np
import casadi as ca
from utils import saturate

class ReVolt:
    def __init__(self, x):
        self.eta    = x[:3] # [x, y, psi]
        self.nu     = x[3:] # [u, v, r]
        self.x      = np.concatenate((self.eta, self.nu), axis=0)
        self.u      = np.zeros(6)

        self.g      = 9.807
        self.rho    = 1025  # kg/V (density of sea water)
        self.m      = 257   # kg
        self.length = 3.02  # m
        self.width  = 0.72  # m
        self.vMax   = 1     # m/s, approx 2 knots

        sl, sw      = self.length/2, self.width/2
        self.vBox   = np.array([[-sl,  sw], [-sl, -sw], [sl, -sw], [sl,  sw]]).T

        # Matrices
        self.M_RB   = np.array([[257, 0, 0], [0, 257, 0], [0, 0, 298]])
        self.M_A    = np.array([[6.93, 0, 0], [0, 49.44, 7.007], [0, 7.028, 24.556]])
        self.M      = self.M_RB + self.M_A
        self.C      = self.getC(self.nu)
        self.D      = np.array([[50.66, 0, 0], [0, 601.45, 83.05], [0, 83.1, 268.17]])

        # Thrusters
        self.lx     = [-1.12, -1.12, 1.08]
        self.ly     = [-0.15,  0.15, 0.00]
        self.tau_max= [ 41, 50, 55]
        self.T_max  = [ 25,  25,  14]
        self.T_min  = [-25, -25, -6.1]
        self.T_e    = np.array([[1, 0, 1, 0, 1, 0],
                                [0, 1, 0, 1, 0, 1],
                                [-self.ly[0], self.lx[0], -self.ly[1], self.lx[1], 0, self.lx[2]]])
        self.K      = np.diag([0.00205, 0.00205, 0.0009])
        self.K_e    = np.diag([0.00205, 0.00205, 0.00205, 0.00205, 0.0009, 0.0009])

        # Casadi matrices
        self.M_ca   = ca.vertcat(ca.horzcat(263.93, 0, 0),
                                 ca.horzcat(0, 306.44, 7.007),
                                 ca.horzcat(0, 7.028, 322.556))
        self.C_ca   = self.getC(self.nu, casadi=True)
        self.D_ca   = ca.vertcat(ca.horzcat(50.66, 0, 0),
                                 ca.horzcat(0, 601.45, 83.05),
                                 ca.horzcat(0, 83.1, 268.17))
        self.T_ca   = ca.vertcat(ca.horzcat(1, 0, 1, 0, 1, 0),
                                 ca.horzcat(0, 1, 0, 1, 0, 1),
                                 ca.horzcat(0, self.lx[0], self.ly[1], -self.lx[1], self.ly[2], -self.lx[2]))

    def getJ(self, psi, use2D=False):
        psi = float(psi)
        J = np.array([[np.cos(psi), -np.sin(psi), 0],
                      [np.sin(psi),  np.cos(psi), 0],
                      [          0,            0, 1]])
        if use2D:
            J = J[:2,:2]
        return J
    
    def getC(self, nu, casadi=False):
        u, v, r = nu[0], nu[1], nu[2]
        if casadi:
            C = ca.vertcat(ca.horzcat(0, 0, -207.56*v+7*r),
                        ca.horzcat(0, 0, 250.07*u),
                        ca.horzcat(207.56*v-7*r, -250.07*u, 0))
        else:
            C = np.array([[0,                    0, -207.56*v+7*r],
                         [0,                    0,      250.07*u],
                         [207.56*v-7*r, -250.07*u,             0]])
        return C

    def getB(self, a):
        """
        Returns B(a) (or T(a)), where a=alpha
        """
        a1, a2, a3      = a[0], a[1], a[2]
        return np.array([[    np.cos(a1),                      np.cos(a2),                    np.cos(a3)],
                         [    np.sin(a1),                      np.sin(a2),                    np.sin(a3)],
                         [-self.ly[0]*np.cos(a1)+self.lx[0]*np.sin(a1),   -self.ly[1]*np.cos(a2)+self.lx[1]*np.sin(a2), self.lx[2]*np.sin(a3)]]).reshape((3,3))

    def getF(self, u):
        """
        Calculate real force vector from applied control inputs.
        => Fi = Ki|ui|ui
        Input: u is the array of thruster inputs, in percentages (-100, +100)
        """
        if u[2] >= 0:
            F2 = float(0.001518 * abs(u[2]) * u[2])
        else:
            F2 = float(0.0006172 * abs(u[2]) * u[2])
            
        return np.array([[float(0.0027 * abs(u[0]) * u[0])],
                         [float(0.0027 * abs(u[1]) * u[1])],
                         [F2]])

    def getTau(self, u, a):
        """
        Calculates tau = B(a)*F(u)
        """
        tau = self.getB(a) @ self.K @ u #self.getF(u)
        
        return tau

    def getCrabAngle(self):
        u, v    = self.nu[0], self.nu[1]
        U       = np.sqrt(u**2 + v**2)
        if U == 0:
            return 0
        return np.arcsin(v/U)

    def step(self, h, u, a):                 
        tau         = self.getTau(u, a)

        eta_dot     = self.getJ(self.eta[2]) @ self.nu
        nu_dot      = (np.linalg.solve(self.M, -(self.D + self.getC(self.nu)) @ self.nu[:,np.newaxis] + tau)).reshape(3)

        self.eta   += h*eta_dot
        self.nu    += h*nu_dot
        return self.eta, self.nu
        
    def plot(self, eta=[], color='blue'):
        if eta == []:
            eta = self.eta

        vVertices = ( (self.getJ(eta[2], use2D=True) @ self.vBox).T + np.tile(np.array([eta[0], eta[1]]), (4, 1)) ).T
        pltLines = np.concatenate((vVertices, vVertices[:,0][:,np.newaxis]), axis=1)

        plt.plot(pltLines[0,:], pltLines[1,:], color=color)