from planner import Action, Plan

class VesselState:

    def __init__(self, state="", remainingActions=[], finishedActions=[]):
        self.state = state
        self.remainingActions = remainingActions
        self.finishedActions = finishedActions

    def updateState(self):
        """
        States: Docked, Docking, Undocking, In transit
        """