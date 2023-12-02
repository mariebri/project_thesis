import numpy as np
from world import World
from revolt import ReVolt
from functions import *

class Control:
    def __init__(self, vessel: ReVolt, world: World):
        self.T  = 2500
        self.ts = 20
        self.eta_tilde_int = np.zeros((3,1))

        self.vessel = vessel
        self.world  = world

    def transit(self, portFrom, portTo):
        x0, u0  = self.vessel.x, self.vessel.u
        path    = self.world.findPath(portFrom, portTo)
        path.insert(0, portFrom)
        print(path)

        for i in range(len(path)-1):
            print('Computing path from %s to %s' % (path[i], path[i+1]))
            eta_des, harbor     = self.world.getTransitInfo(path[i], path[i+1])
            x_opt_n, u_opt_n    = trajectory(eta_des, x0, u0, harbor, self.vessel, self.T, self.ts)
            if 'x_opt' in locals():
                x_opt = np.concatenate((x_opt, x_opt_n), axis=1)
                u_opt = np.concatenate((u_opt, u_opt_n), axis=1)
            else:
                x_opt = x_opt_n
                u_opt = u_opt_n
            x0, u0 = x_opt[:6,-1].T, u_opt[:,-1].T

        self.x_opt, self.u_opt = x_opt, u_opt

        return x_opt, u_opt
    
    def getToEtaD(self, i):
        eta_p               = self.x_opt[:3, i]
        nu_p                = self.x_opt[3:, i]
        uf_p                = self.u_opt[:, i]
        tau, eta_tilde      = PIDcontroller(eta_p, nu_p, self.eta_tilde_int, self.vessel)
        self.eta_tilde_int  = self.eta_tilde_int + self.ts*eta_tilde

        u = thrustAllocation(tau, self.vessel)
        x = self.vessel.step(self.ts, uf_p)
        return x, u