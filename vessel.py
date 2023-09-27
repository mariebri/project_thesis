import numpy as np

class Vessel:

    def __init__(self, x, u_e):
        self.eta = x[:3]    # [x, y, psi]
        self.nu = x[3:]     # [u, v, r]

        self.L = 76.2
        self.g = 9.8
        self.m = 6000e3

        self.lx = np.array([-35, -35, 35])
        self.ly = np.array([7, -7])
    
        self.N = np.diag([1, 1, self.L])
        self.Mbis = np.array([[1.1274, 0, 0],
                              [0, 1.8902, -0.0744],
                              [0, -0.0744, 0.1278]])
        self.Dbis = np.array([[0.0358, 0, 0],
                              [0, 0.1183, -0.0124],
                              [0, -0.0041, 0.0308]])
        
        self.J = self.getJ()
        self.M = self.m*(self.N@self.Mbis@self.N)
        self.D = self.m*np.sqrt(self.g/self.L)*(self.N@self.Dbis@self.N)
        self.u_e = u_e          # u = [u1x, u1y, u2x, u2y, u3]
        self.tau = self.getTau_e(self.u_e)

        self.Tmax_azimuth = (1/30)*self.m
        self.Tmax_tunnel = (1/60)*self.m    # +/-
        self.alphamax = 170*(np.pi/180)     # 170 degrees, +/-
        self.alphamax_rate = 30

    def getJ(self):
        # Rotation matrix
        psi = self.eta[2]
        J = np.array([[np.cos(psi), -np.sin(psi), 0],
                      [np.sin(psi),  np.cos(psi), 0],
                      [          0,            0, 1]])
        return J

    def getT(self, alpha):
        """
        Returns the thrust configuration matrix
            T(a) = [T1, T2, T3]
        where T1, T2 are azimuth thrusters, T3 a tunnels thruster

        Input: alpha = [alpha1, alpha2]
        """
        a1 = alpha[0]
        a2 = alpha[1]
        lx = self.lx
        ly = self.ly
        T = np.array([[                         np.cos(a1),                          np.cos(a2),     0],
                      [                         np.sin(a1),                          np.sin(a2),     1],
                      [lx[0]*np.sin(a1) - ly[0]*np.cos(a1), lx[1]*np.sin(a2) - ly[1]*np.cos(a2), lx[2]] ])
        return T
        
    def getT_e(self):
        """
        Returns the extended thrust configuration matrix
            T_e = [t1x, t1y, t2x, t2y, t3]
        where t1, t2 are azimuth thrusters, t3 a tunnel thruster
        """
        lx = self.lx
        ly = self.ly
        T_e = np.array([[1,          0,      1,     0,     0],
                        [0,          1,      0,     1,     1],
                        [-ly[0], lx[0], -ly[1], lx[1], lx[2]]])
        return T_e

    def getTau_e(self, u_e):
        """
        Returns tau = T_e * u_e

        Based on control allocation:
            tau = T_e * K_e * u_e
        with K_e = I

        Input:
            u_e = [u1x, u1y, u2x, u2y, u3]
        """
        tau = self.getT_e() @ u_e
        return tau
    
    def getTau(self, alpha, f):
        """
        Returns tau = T(a) * f

        Input:
            alpha = [alpha1, alpha2]
            f     = [f1, f2, f3]
        """
        T = self.getT(alpha)
        tau = T @ f

        # Saturation
        if abs(tau[0]) > self.Tmax_azimuth:
            tau[0] = np.sign(tau[0]) * self.Tmax_azimuth

        if abs(tau[1]) > self.Tmax_azimuth:
            tau[1] = np.sign(tau[1]) * self.Tmax_azimuth

        if abs(tau[2]) > self.Tmax_tunnel:
            tau[2] = np.sign(tau[2]) * self.Tmax_tunnel

        return tau

    def dynamics(self, u_e, h):
        """
        Returns x = [eta, nu] after a timestep h

        Based on the following 3-DOF model:
            eta_dot = J(psi)*nu
            nu_dot = inv(M)*(-D*nu + tau)

        Input:
            u_e = [u1x, u1y, u2x, u2y, u3]
            h = timestep

        """

        tau = self.getTau(u_e)
        self.u_e = u_e

        eta_dot = self.J @ self.nu
        nu_dot = np.linalg.solve(self.M, -self.D @ self.nu + tau)

        self.eta += h*eta_dot
        self.nu += h*nu_dot

        x = np.concatenate((self.eta, self.nu))

        return x







