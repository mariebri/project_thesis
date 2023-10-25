import pyplanning as pp

domain_file = "/Planning/simple_domain.pddl"
problem_file = "/Planning/simple_problem.pddl"

domain, problem = pp.load_pddl(domain_file, problem_file)
plan = pp.solvers.graph_plan(problem)

if plan is not None:
    print("Plan found:")
    print(plan, "\n")
else:
    print("Planning failed.")