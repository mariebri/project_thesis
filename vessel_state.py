from utils import PlannerType, State

class VesselState:

    def __init__(self, state=State.DOCKED, fuelLevel=100, replan=False, scenario=1):
        self.state      = state
        self.fuelLevel  = fuelLevel
        self.replan     = replan
        self.low_fuel   = False
        self.scenario   = scenario

        self.port = "porta"

    def updateState(self, state, port):
        self.state  = state
        self.port   = port

    def updateFuelLevel(self, change):
        if self.fuelLevel + change > 100:
            self.fuelLevel = 100
        else:
            self.fuelLevel = self.fuelLevel + change

        # Comment if not in scenario 3
        if self.scenario == 3:
            self.checkFuelLevel()

        print('New fuel level:', self.fuelLevel)

    def checkFuelLevel(self):
        if self.fuelLevel < 40 and not self.replan:
            print('Fuel level too low!')
            print('Need to replan')
            self.low_fuel = True
            raise KeyboardInterrupt