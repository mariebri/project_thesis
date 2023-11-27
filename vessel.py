from enum import Enum
from planner import PlannerType

State = Enum('State', ['DOCKED', 'DOCKING', 'UNDOCKING', 'IN_TRANSIT'])

class Vessel:

    def __init__(self, state=State.DOCKED, fuelLevel=100, replan=False):
        self.state      = state
        self.fuelLevel  = fuelLevel
        self.replan     = replan
        self.low_fuel   = False

    def updateState(self, state):
        self.state = state

    def updateFuelLevel(self, change):
        if self.fuelLevel + change > 100:
            self.fuelLevel = 100
        else:
            self.fuelLevel = self.fuelLevel + change

        # Uncomment if not in scenario 3
        self.checkFuelLevel()

        print('New fuel level:', self.fuelLevel)

    def checkFuelLevel(self):
        if self.fuelLevel < 40 and not self.replan:
            print('Fuel level too low!')
            print('Need to replan')
            self.low_fuel = True
            raise KeyboardInterrupt