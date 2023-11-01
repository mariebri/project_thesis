import pyplanning as pp


# Files for Windows
#domain_file     = "C:/Users/marie/OneDrive/Dokumenter/NTNU/Prosjektoppgave/src/Planning/simple_domain.pddl"
#problem_file    = "C:/Users/marie/OneDrive/Dokumenter/NTNU/Prosjektoppgave/src/Planning/simple_problem.pddl"

# Files for Ubuntu
domain_file     = "/home/marie/project_thesis/Planning/simple_domain.pddl"
problem_file    = "/home/marie/project_thesis/Planning/simple_problem.pddl"


domain, problem = pp.load_pddl(domain_file, problem_file)
plan = pp.solvers.graph_plan(problem)

if plan is not None:
    print("Plan found:")
    print(plan, "\n")
else:
    print("Planning failed.")