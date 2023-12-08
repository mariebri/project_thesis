from utils import *

class VesselState:

    def __init__(self, state=State.DOCKED, battery=100, replan=False, scenario=1):
        self.state      = state
        self.battery    = battery
        self.replan     = replan
        self.low_battery= False
        self.scenario   = scenario

        self.area       = "A-port"
        self.port       = "A"

    def updateState(self, state, area):
        self.state  = state
        self.area   = area
        self.port, _= getPortName(area, state=state)

    def updateBattery(self, change):
        if self.battery + change > 100:
            self.battery = 100
        else:
            self.battery += change

        if self.scenario == 3:
            self.checkBattery()

    def checkBattery(self):
        if self.battery < 40 and not self.replan:
            print('Battery level too low! Replanning at next port...')
            self.low_battery = True

            if self.state == State.DOCKED:
                raise KeyboardInterrupt
        
    def print(self):
        print('Vessel state:\n')
        print('\t State: %s \n\t Battery level: %s \n' % (self.state, str(self.battery)))
        print('\t Area: %s \n\t Port: %s \n' % (self.area, self.port))