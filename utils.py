from enum import Enum

PlannerType = Enum('PlannerType', ['TEMPORAL', 'GRAPHPLAN'])

def getDomainProblemFiles(plannerType: PlannerType, replan=False):
    if plannerType == PlannerType.TEMPORAL:
        domainFile  = "/home/marie/project_thesis/Planning/TEMPORAL/temporal_domain.pddl"
        problemFile = "/home/marie/project_thesis/Planning/TEMPORAL/temporal_problem.pddl"
    elif plannerType == PlannerType.GRAPHPLAN:
        domainFile  = "/home/marie/project_thesis/Planning/CLASSICAL/graphplan_domain.pddl"
        problemFile = "/home/marie/project_thesis/Planning/CLASSICAL/graphplan_problem.pddl"

    if replan:
        problemFile = problemFile = "/home/marie/project_thesis/Planning/replan_problem.pddl"

    return domainFile, problemFile