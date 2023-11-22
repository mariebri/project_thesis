# This module is responsible for replanning, i.e. making new problem files
from vessel_state import VesselState
from utils import *


def makeProblemFile(vessel: VesselState, plannerType: PlannerType):
    initState   = vessel.initPred
    goalState   = vessel.goalPred
    
    # Open a file for writing
    replanFile = '/home/marie/project_thesis/Planning/replan_problem.pddl'
    f   = open(replanFile, "w")

    # Open the original problem file
    _, problemFile = getDomainProblemFiles(plannerType)
    fPF = open(problemFile, "r")

    if plannerType == PlannerType.TEMPORAL:
        domain = "temporal"
    else:
        domain = "graphplan"

    firstLine  = ["(define (problem replan) (:domain " + domain + ")\n"]

    pfLines = fPF.readlines()
    for i in range(len(pfLines)):
        if ":objects" in pfLines[i]:
            objStartIdx = i
            for j in range(i+1, len(pfLines)):
                if ")" in pfLines[j]:
                    objEndIdx = j
                    break

    objectLines = pfLines[objStartIdx:objEndIdx+1] + ["\n"]
    
    initLines   = ["    (:init\n"]
    for state in initState:
        if "=" in state:
            initLines.append("        " + state + "\n")
        elif "intransit" in state:
            # If a vessel is intransit, we simplify and say that
            # the vessel is at the port it was transitting from
            state = state.replace("intransit", "vesselat")
            initLines.append("        (" + state + ")\n")
        else:
            initLines.append("        (" + state + ")\n")
    initLines.append("    )\n")
    initLines.append("\n")

    goalLines   = ["    (:goal (and\n"]
    for state in goalState:
        goalLines.append("        (" + state + ")\n")
    goalLines.append("    ))\n")
    goalLines.append("\n")

    if plannerType == PlannerType.TEMPORAL:
        endLines = ["    (:metric minimize (total-time))\n", ")\n"]
    else:
        endLines = [")\n"]

    lines = firstLine + objectLines + initLines + goalLines + endLines

    for line in lines:
        f.write(line)
    f.close()
    