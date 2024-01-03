from utils import *

class VesselState:

    def __init__(self, state=State.DOCKED, battery=100, replan=False, scenario=1, toArea="A"):
        self.state      = state
        self.battery    = battery
        self.replan     = replan
        self.lowBattery = False
        self.scenario   = scenario

        self.area       = "A-port"
        self.port       = "A-port"
        self.toArea     = toArea

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
            self.lowBattery = True
            print("Battery too low, need to replan...")
            raise NameError("Battery is too low, need to replan...")
        
    def print(self):
        print('Vessel state:\n')
        print('\t State: %s \n\t Battery level: %s \n' % (self.state, str(self.battery)))
        print('\t Area: %s \n\t Port: %s \n' % (self.area, self.port))