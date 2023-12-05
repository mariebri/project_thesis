import numpy as np
from world import World
from revolt import ReVolt
from functions import *

class Control:
    def __init__(self, vessel: ReVolt, world: World):
        self.T  = 2500
        self.ts = 20
        self.h  = 0.1
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
    
    def getToEta(self, eta_des, h):
        steps           = 0
        nu_des          = np.array([0, 0, 0])
        eta_tilde_int   = np.zeros((3,1))

        while not inProximity(self.vessel.eta, eta_des):
            steps          += 1
            tau, eta_tilde  = PIDcontroller(eta_des, nu_des, eta_tilde_int, self.vessel)
            eta_tilde_int   = eta_tilde_int + h*eta_tilde
            u, a            = thrustAllocation(tau, self.vessel)
            eta, nu         = self.vessel.step(h, u, a)
        
        return steps
    
    def transitDubins(self, portFrom, portTo):
        path    = self.world.findPath(portFrom, portTo)
        path.insert(0, portFrom)
        eta0    = self.vessel.eta

        for i in range(len(path)-1):
            print('Computing path from %s to %s' % (path[i], path[i+1]))
            eta_des, _  = self.world.getTransitInfo(path[i], path[i+1])
            eta         = dubinsPath(eta_start=eta0, eta_end=eta_des)

            if 'eta_opt' in locals():
                eta_opt = np.concatenate((eta_opt, eta), axis=1)
            else:
                eta_opt = eta
            eta0 = eta_opt[:,-1]

        return eta_opt