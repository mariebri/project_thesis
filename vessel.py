from enum import Enum
from planner import PlannerType

State = Enum('State', ['DOCKED', 'DOCKING', 'UNDOCKING', 'IN_TRANSIT'])

class Vessel:

    def __init__(self, state=State.DOCKED, fuelLevel=100):
        self.state      = state
        self.fuelLevel  = fuelLevel

    def updateState(self, state):
        self.state = state