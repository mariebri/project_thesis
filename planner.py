import os
import subprocess
import pyplanning as pp
from enum import Enum

PlannerType = Enum('PlannerType', ['TEMPORAL', 'GRAPHPLAN'])

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

class Plan:
    def __init__(self, domainFile, problemFile, planner: PlannerType, algorithm="stp-2"):
        self.domainFile = domainFile
        self.problemFile = problemFile
        self.planner = planner
        self.algorithm = algorithm

        self.planFile = self.computePlanFile()
        self.actions = self.actionsFromPlanFile()

        self.initPred, self.goalPred = self.getPredicates()

    def getActions(self):
        return self.actions

    def printPlan(self):
        i = 1
        for a in self.actions:
            print(i, ":", a.getAction(), a.getPredicates())
            i += 1

    def computePlanFile(self):
        if self.planner == PlannerType.TEMPORAL:
            try:
                cmd0 = "cd"
                cmd1 = ". temporal-planning-test/bin/activate"
                cmd2 = "cd temporal-planning-test/temporal-planning/"
                cmd3 = "python2.7 bin/plan.py " + self.algorithm + " " + self.domainFile + " " + self.problemFile
                cmd  = cmd0 + "; " + cmd1 + "; " + cmd2 + "; " + cmd3
                os.system(cmd)

            except subprocess.TimeoutExpired as timeErr:
                print("Process timeout")

            planFile = "/home/marie/temporal-planning-test/temporal-planning/tmp_sas_plan.1"

        elif self.planner == PlannerType.GRAPHPLAN:
            domain, problem = pp.load_pddl(self.domainFile, self.problemFile)
            planFile = pp.solvers.graph_plan(problem)

        else:
            print("Invalid PlannerType")
            return

        return planFile

    def actionsFromPlanFile(self):
        actions = []

        if self.planner == PlannerType.TEMPORAL:
            with open(self.planFile) as f:
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
            for i in range(len(self.planFile)):
                i += 1
                line = self.planFile[i].pop()
                action = line.action.name
                predicates = [str(o) for o in line.objects]
                addEffects, delEffects = self.getEffects(action, predicates)
                action = Action(action, predicates, addEffects, delEffects, self.planner)
                actions.append(action)     
        
        return actions

    def getPredicates(self):
        # Reads from the problem file and returns a list of all true initial and goal predicates
        initPred, goalPred = [], []

        f       = open(self.problemFile, "r")
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

        f       = open(self.domainFile, "r")
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
