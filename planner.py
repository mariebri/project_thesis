import os
import sys
import shutil
import subprocess
import time
import copy
import math
import pyplanning as pp
from utils import *
from vessel_state import *
from replanner import Replanner

class Action:
    def __init__(self, action, parameters, addEffects, delEffects, planner: PlannerType, start=0.0, dur=0.0):
        self.action = action
        self.parameters = parameters
        self.addEffects = addEffects
        self.delEffects = delEffects
        self.planner = planner
        self.start = float(start)
        self.dur = float(dur)

    def getAction(self):
        return self.action
    
    def getParameters(self):
        return self.parameters
    
    def getEffects(self):
        return self.addEffects, self.delEffects
    
    def getPlanner(self):
        return self.planner

    def getStartTime(self):
        return self.start
    
    def getEndTime(self):
        return self.start + self.dur

class Planner:
    def __init__(self, planner: PlannerType, algorithm="stp-2", replan=False, fuelLevel=100, scenario=1):
        self.domain, self.problem   = getDomainProblemFiles(plannerType=planner, replan=replan, scenario=scenario)
        self.planner                = planner
        self.algorithm              = algorithm
        self.replan                 = replan
        self.fuelLevel              = fuelLevel
        self.scenario               = scenario

        self.plan, self.compTime    = self.computePlan()
        self.actions                = self.getActionsFromPlan()

    def printPlan(self):
        for a in self.actions:
            print(a.getStartTime(), ":", a.getAction(), a.getParameters())

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
                    parameters = actionLine[1:]
                    dur = l[2].strip()
                    addEffects, delEffects = self.getEffects(action, parameters)
                    action = Action(action, parameters, addEffects, delEffects, self.planner, start, dur)
                    actions.append(action)

        elif self.planner == PlannerType.GRAPHPLAN:
            for i in range(len(self.plan)):
                i += 1
                for line in self.plan[i]:
                    #line = self.plan[i].pop()
                    action = line.action.name
                    parameters = [str(o) for o in line.objects]
                    addEffects, delEffects = self.getEffects(action, parameters)
                    action = Action(action, parameters, addEffects, delEffects, self.planner, start=i)
                    actions.append(action)
        return actions

    def getPredicates(self, startPos=False):
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

        if startPos:
            for pred in initPred:
                if "vesselat" in pred:
                    port = pred[2]
                    return initPred, goalPred, port

        return initPred, goalPred
    
    def getEffects(self, action, param):
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

                # Finding parameters
                paramString = ""
                elem = l.split(' ')
                for e in elem:
                    if "?" in e:
                        paramIndex = parameters.index(e)
                        paramString = paramString + " " + param[paramIndex]

                if "not" in l:
                    effect = elem[3]
                    if "at start" in l:
                        delAtStart.append(effect + paramString)
                    elif "at end" in l:
                        delAtEnd.append(effect + paramString)
                else:
                    effect = elem[2]
                    if "at start" in l:
                        addAtStart.append(effect + paramString)
                    elif "at end" in l:
                        addAtEnd.append(effect + paramString)

            addEffects = [addAtStart, addAtEnd]
            delEffects = [delAtStart, delAtEnd]

        elif self.planner == PlannerType.GRAPHPLAN:

            for i in range(effectIndex+1, end):
                l = lines[i]
                if l == "":
                    break
                
                # Finding parameters
                paramString = ""
                elem = l.split(' ')
                for e in elem:
                    if "?" in e:
                        paramIndex = parameters.index(e)
                        paramString = paramString + " " + param[paramIndex]

                if "not" in l:
                    effect = elem[1]
                    delEffects.append(effect + paramString)
                else:
                    effect = elem[0]
                    addEffects.append(effect + paramString)

        return addEffects, delEffects
