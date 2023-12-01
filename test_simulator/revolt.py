import matplotlib.pyplot as plt
import numpy as np
import casadi as ca

class ReVolt:
    def __init__(self, x):
        self.eta    = x[:3] # [x, y, psi]
        self.nu     = x[3:] # [u, v, r]

        self.g      = 9.807
        self.rho    = 1025  # kg/V (density of sea water)
        self.m      = 257   # kg
        self.length = 3.02  # m
        self.width  = 0.72  # m

        sl, sw      = self.length/2, self.width/2
        self.vBox   = np.array([[-sl,  sw], [-sl, -sw], [sl, -sw], [sl,  sw]]).T

        # Matrices
        self.M_RB   = np.array([[257, 0, 0], [0, 257, 0], [0, 0, 298]])
        self.M_A    = np.array([[6.93, 0, 0], [0, 49.44, 7.007], [0, 7.028, 24.556]])
        self.M      = self.M_RB + self.M_A
        self.C      = self.getC(self.nu)
        self.D      = np.array([[50.66, 0, 0], [0, 601.45, 83.05], [0, 83.1, 268.17]])

        # Thrusters
        lx1, lx2, lx3   = -1.65, -1.65, 1.15
        ly1, ly2, ly3   = -0.15,  0.15, 0.00
        self.T_max  = [ 25,  25,  14]
        self.T_min  = [-25, -25, -6.1]
        self.T_e    = np.array([[1, 0, 1, 0, 1, 0], [0, 1, 0, 1, 0, 1], [0, lx1, ly2, -lx2, ly3, -lx3]])

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
                                 ca.horzcat(0, lx1, ly2, -lx2, ly3, -lx3))

    def getJ(self, use2D=False):
        psi = np.float(self.eta[2])
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

    def getT_a(self, alpha=[0,0,np.pi/2]):
        a1, a2, a3      = alpha[0], alpha[1], alpha[2]
        lx1, lx2, lx3   = -1.65, -1.65, 1.15
        ly1, ly2, ly3   = -0.15,  0.15, 0.00
        return np.array([[    np.cos(a1),                      np.cos(a2),                    np.cos(a3)],
                         [    np.sin(a1),                      np.sin(a2),                    np.sin(a3)],
                         [lx1*np.sin(a1),   ly2*np.cos(a2)-lx2*np.sin(a2), ly3*np.cos(a3)-lx3*np.sin(a3)]])

    def step(self, h, u):
        tau         = self.T_e @ u

        eta_dot     = self.getJ() @ self.nu
        nu_dot      = np.linalg.solve(self.M, -(self.D + self.getC(self.nu)) @ self.nu + tau)

        self.eta    = self.eta + h*eta_dot
        self.nu     = self.nu + h*nu_dot
        x           = np.concatenate((self.eta, self.nu), axis=0)
        return x
        
    def plot(self, eta=[]):
        if eta == []:
            x = self.eta[0]
            y = self.eta[1]
        else:
            x = eta[0]
            y = eta[1]

        vVertices = ( (self.getJ(use2D=True) @ self.vBox).T + np.tile(np.array([x, y]), (4, 1)) ).T
        pltLines = np.concatenate((vVertices, vVertices[:,0][:,np.newaxis]), axis=1)

        plt.plot(pltLines[0,:], pltLines[1,:], color='blue')