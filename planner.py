import os
import subprocess

def plan():
    try:
        pathToExecute = '/home/marie/optic-clp-release/./optic-clp'
        result = subprocess.run([pathToExecute, 'Planning/domain.pddl', 'Planning/problem.pddl'], capture_output=True, text=True, timeout=20)
        output = result.stdout
        write_per = "w"
    except subprocess.TimeoutExpired as timeErr:
        print("Process timeout")
        output = timeErr.stdout
        write_per = "wb"

    planFile = "Planning/results.txt"
    f = open(planFile, write_per)
    f.write(output)
    f.close()

if __name__ == '__main__':
    plan()
