from enum import Enum
from planner import PlannerType

State = Enum('State', ['DOCKED', 'DOCKING', 'UNDOCKING', 'IN_TRANSIT'])

class VesselState:

    def __init__(self, state="State.DOCKED", remainingActions=[], finishedActions=[], initPred=[], goalPred=[]):
        self.state              = state
        self.remainingActions   = remainingActions
        self.finishedActions    = finishedActions
        self.allActions         = remainingActions + finishedActions
        self.initPred           = initPred
        self.goalPred           = goalPred

    def updateActions(self, finishedAction):
        # Update the action lists
        self.remainingActions.remove(finishedAction)
        self.finishedActions.append(finishedAction)

    def updatePredStart(self, startedAction):
        # Only used for temporal planners
        addEffects, delEffects = startedAction.getEffects()
        addEffects = addEffects[0]
        delEffects = delEffects[0]

        print('\n AT START:')
        print('Add effects: ', addEffects)
        print('Del effects: ', delEffects)
        print('')

        # Update
        effInPred = [False for i in range(len(addEffects))]
        for pred in self.initPred:
            for i in range(len(addEffects)):
                if pred == addEffects[i]:
                    effInPred[i] = True
            for eff in delEffects:
                if pred == eff:
                    self.initPred.remove(pred)
        
        for i in range(len(effInPred)):
            if not effInPred[i]:
                self.initPred.append(addEffects[i])

        for pred in self.goalPred:
            for eff in addEffects:
                if pred == eff:
                    self.goalPred.remove(pred)

        print('Initial: ')
        print(self.initPred)
        print('Goal: ')
        print(self.goalPred)

    def updatePredEnd(self, finishedAction):
        addEffects, delEffects = finishedAction.getEffects()

        if finishedAction.getPlanner() == PlannerType.TEMPORAL:
            addEffects = addEffects[1]
            delEffects = delEffects[1]

        print('\n AT END:')
        print('Add effects: ', addEffects)
        print('Del effects: ', delEffects)
        print('')

        # Update
        effInPred = [False for i in range(len(addEffects))]
        for pred in self.initPred:
            for i in range(len(addEffects)):
                if pred == addEffects[i]:
                    effInPred[i] = True
            for eff in delEffects:
                if pred == eff:
                    self.initPred.remove(pred)
        
        for i in range(len(effInPred)):
            if not effInPred[i]:
                self.initPred.append(addEffects[i])

        for pred in self.goalPred:
            for eff in addEffects:
                if pred == eff:
                    self.goalPred.remove(pred)

        print('Initial: ')
        print(self.initPred)
        print('Goal: ')
        print(self.goalPred)

    def updateState(self, state):
        self.state = state