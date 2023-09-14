import subprocess

def plan():
    try:
        pathToExecute = ...
        result = subprocess.run([pathToExecute, 'PDDL/domain.pddl', 'PDDL/problem.pddl'], capture_output=True, text=True, timeout=20)
        output = result.stdout
        write_per = "w"
    except subprocess.TimeoutExpired as timeErr:
        print("Process timeout")
        output = timeErr.stdout
        write_per = "wb"

    planFile = "PDDL/results.txt"
    f = open(planFile, write_per)
    f.write(output)
    f.close()
