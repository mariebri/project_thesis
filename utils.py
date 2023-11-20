from planner import PlannerType

def getDomainProblemFiles(plannerType: PlannerType, replan=False):
    if plannerType == PlannerType.TEMPORAL:
        domainFile  = "/home/marie/project_thesis/Planning/temporal_domain.pddl"
        problemFile = "/home/marie/project_thesis/Planning/temporal_problem.pddl"
    elif plannerType == PlannerType.GRAPHPLAN:
        domainFile  = "/home/marie/project_thesis/Planning/simple_domain.pddl"
        problemFile = "/home/marie/project_thesis/Planning/simple_problem.pddl"

    if replan:
        problemFile = problemFile = "/home/marie/project_thesis/Planning/replan_problem.pddl"

    return domainFile, problemFile