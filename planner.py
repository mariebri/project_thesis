import os
import sys
import shutil
import subprocess
import time
import copy
import pyplanning as pp
from utils import *
from vessel import *
from replanner import Replanner

class Action:
    def __init__(self, action, predicates, addEffects, delEffects, planner: PlannerType, start=0.0, end=0.0):
        self.action = action
        self.predicates = predicates
        self.addEffects = addEffects
        self.delEffects = delEffects
        self.planner = planner
        self.start = float(start)
        self.end = float(end)

    def getAction(self):
        return self.action
    
    def getPredicates(self):
        return self.predicates
    
    def getEffects(self):
        return self.addEffects, self.delEffects
    
    def getPlanner(self):
        return self.planner

    def getStartTime(self):
        return self.start
    
    def getEndTime(self):
        return self.end
    
    def getDuration(self):
        return self.end - self.start

class Planner:
    def __init__(self, planner: PlannerType, algorithm="stp-2", replan=False, fuelLevel=100):
        self.domain, self.problem   = getDomainProblemFiles(plannerType=planner, replan=replan)
        self.planner                = planner
        self.algorithm              = algorithm

        self.plan, self.compTime    = self.computePlan()
        self.actions                = self.getActionsFromPlan()
        self.init, self.goal        = self.getPredicates()

        self.remainingActions       = copy.deepcopy(self.actions)
        self.finishedActions        = []
        self.allActions             = self.remainingActions + self.finishedActions

        self.vessel = Vessel(fuelLevel=fuelLevel, replan=replan)

    def printPlan(self):
        for a in self.actions:
            print(a.getStartTime(), ":", a.getAction(), a.getPredicates())

    def computePlan(self):
        start = time.time()
        if self.planner == PlannerType.TEMPORAL:
            try:
                cmd0 = "cd"
                cmd1 = ". temporal-planning-test/bin/activate"
                cmd2 = "cd temporal-planning-test/temporal-planning/"
                cmd3 = "python2.7 bin/plan.py " + self.algorithm + " " + self.domain + " " + self.problem
                cmd  = cmd0 + "; " + cmd1 + "; " + cmd2 + "; " + cmd3
                os.system(cmd)
                end = time.time()

            except subprocess.TimeoutExpired as timeErr:
                print("Process timeout")

            # Choosing the plan file with the lowest total time
            planFile1   = "/home/marie/temporal-planning-test/temporal-planning/tmp_sas_plan.1"
            planFile2   = "/home/marie/temporal-planning-test/temporal-planning/tmp_sas_plan.2"
            plan1       = "/home/marie/temporal-planning-test/temporal-planning/plan1"
            plan2       = "/home/marie/temporal-planning-test/temporal-planning/plan2"

            if os.path.exists(planFile2):
                f1 = open(planFile1, "r")
                f2 = open(planFile2, "r")
                time1 = float((f1.readlines()[-1]).split(':')[0])
                time2 = float((f2.readlines()[-1]).split(':')[0])
                f1.close(), f2.close()

                shutil.copyfile(planFile1, plan1)
                shutil.copyfile(planFile2, plan2)
                os.remove(planFile1), os.remove(planFile2)

                if time1 < time2:
                    plan = plan1
                    print("Using planFile no. 1")
                else:
                    plan = plan2
                    print("Using planFile no. 2")
                
            else:
                shutil.copyfile(planFile1, plan1)
                plan = plan1
                os.remove(planFile1)

        elif self.planner == PlannerType.GRAPHPLAN:
            _, problem = pp.load_pddl(self.domain, self.problem)
            plan = pp.solvers.graph_plan(problem, print_debug=True)
            end = time.time()
            print(plan)

        else:
            print("Invalid PlannerType")
            return

        computationTime = end - start
        return plan, computationTime

    def getActionsFromPlan(self):
        actions = []

        if self.planner == PlannerType.TEMPORAL:
            with open(self.plan) as f:
                for l in f:
                    l = l.replace(")", "(").replace(":"," ").replace("["," ").replace("]"," ")
                    l = l.strip().split('(')

                    # Creating a new Action for each line
                    start = l[0].strip()
                    actionLine = l[1].split()
                    action = actionLine[0]
                    predicates = actionLine[1:]
                    end = l[2].strip()
                    addEffects, delEffects = self.getEffects(action, predicates)
                    action = Action(action, predicates, addEffects, delEffects, self.planner, start, end)
                    actions.append(action)

        elif self.planner == PlannerType.GRAPHPLAN:
            for i in range(len(self.plan)):
                i += 1
                for line in self.plan[i]:
                    #line = self.plan[i].pop()
                    action = line.action.name
                    predicates = [str(o) for o in line.objects]
                    addEffects, delEffects = self.getEffects(action, predicates)
                    action = Action(action, predicates, addEffects, delEffects, self.planner, start=i)
                    actions.append(action)
        return actions

    def getPredicates(self):
        # Reads from the problem file and returns a list of all true initial and goal predicates
        initPred, goalPred = [], []

        f       = open(self.problem, "r")
        lines   = f.readlines()
        end     = len(lines)
        f.close()

        # Formatting lines: removing parantheses and comments
        for i in range(end):
            lines[i] = (lines[i].split(';')[0]).strip()
            if "=" not in lines[i]:
                lines[i] = lines[i].replace(')','').replace('(','')
        
        for i in range(end):
            if "init" in lines[i]:
                for j in range(i+1, end):
                    if (lines[j] == ""):
                        break
                    initPred.append(lines[j])
            if "goal" in lines[i]:
                for j in range(i+1, end):
                    if (lines[j] == ""):
                        break
                    goalPred.append(lines[j])

        return initPred, goalPred
    
    def getEffects(self, action, predicates):
        # Reads from the domain file and returns a list of all add and del effects
        addEffects, delEffects = [], []

        f       = open(self.domain, "r")
        lines   = f.readlines()
        end     = len(lines)
        f.close()

        # Formatting lines: removing parantheses and comments
        for i in range(end):
            lines[i] = (lines[i].split(';')[0]).strip()
            lines[i] = lines[i].replace(')','').replace('(','')

        for i in range(end):
            if "action " + action in lines[i]:
                for j in range(i+1, end):
                    if "parameters" in lines[j]:
                        parameterLine = lines[j]
                    if "effect" in lines[j]:
                        effectIndex = j
                        break

        # Map predicates to parameters
        parameters = ((parameterLine.replace(':parameters ', '').replace('-','')).strip()).split()
        for p in parameters:
            if "?" not in p:
                parameters.remove(p)


        if self.planner == PlannerType.TEMPORAL:
            addAtStart, addAtEnd, delAtStart, delAtEnd = [], [], [], []

            for i in range(effectIndex+1, end):
                l = lines[i]
                if l == "":
                    break

                # Finding predicates
                predString = ""
                elem = l.split(' ')
                for e in elem:
                    if "?" in e:
                        predIndex = parameters.index(e)
                        predString = predString + " " + predicates[predIndex]

                if "not" in l:
                    effect = elem[3]
                    if "at start" in l:
                        delAtStart.append(effect + predString)
                    elif "at end" in l:
                        delAtEnd.append(effect + predString)
                else:
                    effect = elem[2]
                    if "at start" in l:
                        addAtStart.append(effect + predString)
                    elif "at end" in l:
                        addAtEnd.append(effect + predString)

            addEffects = [addAtStart, addAtEnd]
            delEffects = [delAtStart, delAtEnd]

        elif self.planner == PlannerType.GRAPHPLAN:

            for i in range(effectIndex+1, end):
                l = lines[i]
                if l == "":
                    break
                
                # Finding predicates
                predString = ""
                elem = l.split(' ')
                for e in elem:
                    if "?" in e:
                        predIndex = parameters.index(e)
                        predString = predString + " " + predicates[predIndex]

                if "not" in l:
                    effect = elem[1]
                    delEffects.append(effect + predString)
                else:
                    effect = elem[0]
                    addEffects.append(effect + predString)

        return addEffects, delEffects

    def executePlan(self):
        actions = self.allActions
        for a in actions:
            try:
                self.executeAction(a)
            except KeyboardInterrupt:
                print('\nReplanning')
                replanner = Replanner(self.init, self.goal, self.planner)

                if self.vessel.low_fuel:
                    print('Low fuel...')
                    replanner.makeProblemFile(low_fuel=True)
                    os.system('python3 main.py True %s' % self.vessel.fuelLevel)
                    sys.exit()
                
                replanner.makeProblemFile()
                print('Made replan problem file')
                time.sleep(10)
                os.system('python3 main.py True 100')
                sys.exit()
            self.updateActions(a)
            self.updatePredEnd(a)

    def executeAction(self, a: Action):
        action  = a.getAction()
        pred    = a.getPredicates()
        start   = a.getStartTime()

        if action == "transit":
            self.vessel.updateState(State.IN_TRANSIT)
            self.updatePredStart(a)

            portFrom    = pred[0]
            portTo      = pred[1]
            print("At %f\n Transit from %s to %s\n" % (start, portFrom, portTo))
            for i in range(3):
                self.vessel.updateFuelLevel(-5)
                time.sleep(1)

        elif action == "undock":
            self.vessel.updateState(State.UNDOCKING)
            self.updatePredStart(a)

            port = pred[0]
            print("At %f\n Undocking at %s\n" % (start, port))
            for i in range(1):
                self.vessel.updateFuelLevel(-5)
                time.sleep(1)

        elif action == "dock":
            self.vessel.updateState(State.DOCKING)
            self.updatePredStart(a)

            port = pred[0]
            print("At %f\n Docking at %s\n" % (start, port))
            for i in range(1):
                self.vessel.updateFuelLevel(-5)
                time.sleep(1)

        elif action == "load":
            self.vessel.updateState(State.DOCKED)
            self.updatePredStart(a)

            port = pred[0]
            goods = pred[1]
            print("At %f\n Loading %s at %s\n" % (start, goods, port))
            time.sleep(3)

        elif action == "unload":
            self.vessel.updateState(State.DOCKED)
            self.updatePredStart(a)

            port = pred[0]
            goods = pred[1]
            print("At %f\n Unloading %s at %s\n" % (start, goods, port))
            time.sleep(3)

        elif action == "fuelling":
            self.vessel.updateState(State.DOCKED)
            self.updatePredStart(a)

            port = pred[0]
            print("At %f\n Fuelling at %s\n" % (start, port))
            for i in range(5):
                self.vessel.updateFuelLevel(20)
                time.sleep(1)

            # Uncomment if not in scenario 3
            self.vessel.low_fuel = False
            raise KeyboardInterrupt

        else:
            raise Exception("Not a valid action name")
        
    def updateActions(self, finishedAction: Action):
        self.remainingActions.remove(finishedAction)
        self.finishedActions.append(finishedAction)

    def updatePredStart(self, startedAction: Action):
        if self.planner == PlannerType.TEMPORAL:
            # Only used for temporal planners
            addEffects, delEffects = startedAction.getEffects()
            addEffects = addEffects[0]
            delEffects = delEffects[0]

            # Update
            effInPred = [False for i in range(len(addEffects))]
            for pred in self.init:
                for i in range(len(addEffects)):
                    if pred == addEffects[i]:
                        effInPred[i] = True
                for eff in delEffects:
                    if pred == eff:
                        self.init.remove(pred)
            
            for i in range(len(effInPred)):
                if not effInPred[i]:
                    self.init.append(addEffects[i])

            for pred in self.goal:
                for eff in addEffects:
                    if pred == eff:
                        self.goal.remove(pred)
        else:
            return

    def updatePredEnd(self, finishedAction: Action):
        addEffects, delEffects = finishedAction.getEffects()

        if self.planner == PlannerType.TEMPORAL:
            addEffects = addEffects[1]
            delEffects = delEffects[1]

        # Update
        effInPred = [False for i in range(len(addEffects))]
        for pred in self.init:
            for i in range(len(addEffects)):
                if pred == addEffects[i]:
                    effInPred[i] = True
            for eff in delEffects:
                if pred == eff:
                    self.init.remove(pred)
        
        for i in range(len(effInPred)):
            if not effInPred[i]:
                self.init.append(addEffects[i])

        for pred in self.goal:
            for eff in addEffects:
                if pred == eff:
                    self.goal.remove(pred)
