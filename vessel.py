import numpy as np

class Vessel:

    def __init__(self, x, u):
        self.eta = x[:3]    # [x, y, psi]
        self.nu = x[3:]     # [u, v, r]

        self.L = 76.2
        self.g = 9.8
        self.m = 6000e3
    
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
        self.u = u          # u = [f1, f2, f3, alpha1, alpha2]
        self.tau = self.getTau(self.u)

    def getJ(self):
        # Rotation matrix
        psi = self.eta[2]
        J = np.array([[np.cos(psi), -np.sin(psi), 0],
                      [np.sin(psi),  np.cos(psi), 0],
                      [          0,            0, 1]])
        return J

    def getTau(self, u):
        # Control input vector, tau = T(a)*f
        # u = [f1, f2, f3, alpha1, alpha2]
        lx = np.array([-35, -35, 35])
        ly = np.array([7, -7])
        alpha = np.array([u[3], u[4], np.pi/2])
        f = u[:3]

        tau = np.array([f[0]*np.cos(alpha[0]) + f[1]*np.cos(alpha[1]),
                        f[0]*np.sin(alpha[0]) + f[1]*np.sin(alpha[1]) + f[2],
                        f[0]*(lx[0]*np.sin(alpha[0]) - ly[0]*np.cos(alpha[0])) + f[1]*(lx[1]*np.sin(alpha[1]) - ly[1]*np.cos(alpha[1])) + f[2]*lx[2]])
        return tau
    
    def dynamics(self, u, h):
        """
        Returns x = [eta, nu] after a timestep h

        Based on the following 3-DOF model:
            eta_dot = J(psi)*nu
            nu_dot = inv(M)*(-D*nu + tau)

        Input:
            u = [f1, f2, f3, alpha1, alpha2]
            h = timestep

        """

        tau = self.getTau(u)

        eta_dot = self.J @ self.nu
        nu_dot = np.linalg.solve(self.M, -self.D @ self.nu + tau)

        self.eta += h*eta_dot
        self.nu += h*nu_dot

        x = np.concatenate((self.eta, self.nu))

        return x







