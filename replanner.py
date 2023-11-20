# This module is responsible for replanning, i.e. making new problem files
from vessel_state import VesselState
from planner import PlannerType


def makeProblemFile(vessel: VesselState, fileName, plannerType: PlannerType):
    initState   = vessel.initPred
    goalState   = vessel.goalPred
    
    # Open a file for writing
    f = open(fileName, "w")

    if plannerType == PlannerType.TEMPORAL:
        domain = "temporal"
    else:
        domain = "graphplan"

    firstLines  = ["(define (problem replan) (:domain " + domain + ")\n",
                  "    (:objects\n",
                  "        vessel0 - vessel\n",
                  "        porta portb portc portd porte - port\n",
                  "        goodsab goodsce goodscd - goods\n",
                  "    )\n",
                  "\n"]
    
    initLines   = ["    (:init\n"]
    for state in initState:
        if "=" not in state:
            initLines.append("        (" + state + ")\n")
        else:
            initLines.append("        " + state + "\n")
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

    lines = firstLines + initLines + goalLines + endLines

    for line in lines:
        f.write(line)
    f.close()
    