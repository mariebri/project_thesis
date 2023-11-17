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
                  "\t(:objects\n",
                  "\t\tvessel0 - vessel\n",
                  "\t\tporta portb portc portd porte - port\n",
                  "\t\tgoodsab goodsce goodscd - goods\n",
                  "\t)\n",
                  "\n"]
    
    initLines   = ["\t(:init\n"]
    for state in initState:
        if "=" not in state:
            initLines.append("\t\t(" + state + ")\n")
        else:
            initLines.append("\t\t" + state + "\n")
    initLines.append("\t)\n")
    initLines.append("\n")

    goalLines   = ["\t(:goal (and\n"]
    for state in goalState:
        goalLines.append("\t\t(" + state + ")\n")
    goalLines.append("\t))\n")
    goalLines.append("\n")

    if plannerType == PlannerType.TEMPORAL:
        endLines = ["\t(:metric minimize (total-time))\n", ")\n"]
    else:
        endLines = [")\n"]

    lines = firstLines + initLines + goalLines + endLines

    for line in lines:
        f.write(line)
    f.close()
    