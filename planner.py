import os
import subprocess
import pyplanning as pp

class Action:
    def __init__(self, action, predicates, start=0.0, end=0.0):
        self.action = action
        self.predicates = predicates
        self.start = float(start)
        self.end = float(end)

    def getAction(self):
        return self.action
    
    def getPredicates(self):
        return self.predicates
    
    def getStartTime(self):
        return self.start
    
    def getEndTime(self):
        return self.end
    
    def getDuration(self):
        return self.end - self.start

class Plan:
    def __init__(self, actions):
        self.actions = actions

    def printPlan(self):
        i = 1
        for a in self.actions:
            print(i, ":", a.getAction(), a.getPredicates())
            i += 1

def makePlanFromFile(planFile, planner):
    actions = []

    if planner == "temporal":
        with open(planFile) as f:
            for l in f:
                l = l.replace(")", "(").replace(":"," ").replace("["," ").replace("]"," ")
                l = l.strip().split('(')

                # Creating a new Action for each line
                start = l[0].strip()
                actionLine = l[1].split()
                action = actionLine[0]
                predicates = actionLine[1:]
                end = l[2].strip()
                action = Action(action, predicates, start, end)
                actions.append(action)

    elif planner == "graphplan":
        for i in range(len(planFile)):
            i += 1
            line = planFile[i].pop()
            action = line.action.name
            predicates = [str(o) for o in line.objects]
            action = Action(action, predicates)
            actions.append(action)     
    
    plan = Plan(actions)
    plan.printPlan()
    return plan

def computePlan(planner="temporal"):
    if planner == "temporal":
        try:
            domain_file     = "/home/marie/project_thesis/Planning/temporal_domain.pddl"
            problem_file    = "/home/marie/project_thesis/Planning/temporal_problem.pddl"
            algorithm       = "stp-2"

            cmd0 = "cd"
            cmd1 = ". temporal-planning-test/bin/activate"
            cmd2 = "cd temporal-planning-test/temporal-planning/"
            cmd3 = "python2.7 bin/plan.py " + algorithm + " " + domain_file + " " + problem_file
            cmd  = cmd0 + "; " + cmd1 + "; " + cmd2 + "; " + cmd3
            os.system(cmd)

        except subprocess.TimeoutExpired as timeErr:
            print("Process timeout")

        planFile = "/home/marie/temporal-planning-test/temporal-planning/tmp_sas_plan.1"
        plan = makePlanFromFile(planFile, planner=planner)

    elif planner == "graphplan":
        domain_file     = "/home/marie/project_thesis/Planning/simple_domain.pddl"
        problem_file    = "/home/marie/project_thesis/Planning/simple_problem.pddl"

        domain, problem = pp.load_pddl(domain_file, problem_file)
        plan = pp.solvers.graph_plan(problem)

        if plan is not None:
            plan = makePlanFromFile(plan, planner=planner)
        else:
            print("Planning failed.")

    else:
        print("Error - Invalid planner type")

    return plan


if __name__ == '__main__':
    plan = computePlan(planner="temporal")
