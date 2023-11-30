from enum import Enum

PlannerType = Enum('PlannerType', ['TEMPORAL', 'GRAPHPLAN'])

def getDomainProblemFiles(plannerType: PlannerType, scenario=1, replan=False):
    if plannerType == PlannerType.TEMPORAL:
        domainFile  = "/home/marie/project_thesis/Planning/TEMPORAL/domain.pddl"
        if scenario == 1:
            problemFile = "/home/marie/project_thesis/Planning/TEMPORAL/p1.pddl"
        elif scenario == 2:
            problemFile = "/home/marie/project_thesis/Planning/TEMPORAL/p2.pddl"
        elif scenario == 3:
            problemFile = "/home/marie/project_thesis/Planning/TEMPORAL/p3.pddl"

    elif plannerType == PlannerType.GRAPHPLAN:
        domainFile  = "/home/marie/project_thesis/Planning/CLASSICAL/domain.pddl"
        if scenario == 1:
            problemFile = "/home/marie/project_thesis/Planning/CLASSICAL/p1.pddl"
        elif scenario == 2:
            problemFile = "/home/marie/project_thesis/Planning/CLASSICAL/p2.pddl"
        elif scenario == 3:
            problemFile = "/home/marie/project_thesis/Planning/CLASSICAL/p3.pddl"

    if replan:
        problemFile = "/home/marie/project_thesis/Planning/replan_problem.pddl"

    return domainFile, problemFile