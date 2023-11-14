import os
import subprocess

class Action:
    def __init__(self, start, action, predicates, end):
        self.start = start
        self.action = action
        self.predicates = predicates
        self.end = end

    def getAction(self):
        return self.action
    
    def getPredicates(self):
        return self.predicates


class Plan:
    def __init__(self, actions):
        self.actions = actions

    def printPlan(self):
        i = 1
        for a in self.actions:
            print(i, ":", a.getAction(), a.getPredicates())
            i += 1



def makePlanFromFile(planFile):
    actions = []
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
            action = Action(start, action, predicates, end)
            actions.append(action)
    
    plan = Plan(actions)
    plan.printPlan()
    return plan


def plan():
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
    plan = makePlanFromFile(planFile)
            


if __name__ == '__main__':
    plan()
