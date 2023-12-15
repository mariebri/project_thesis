from utils import *
from planner import Planner

class Replanner():
    def __init__(self, init, goal, origPlan, battery=100, lowBattery=False, port0="A"):
        self.init       = init
        self.goal       = goal

        self.planner    = origPlan.planner
        self.algorithm  = origPlan.algorithm
        self.scenario   = origPlan.scenario

        self.battery    = battery
        self.lowBattery = lowBattery
        self.port0      = port0

        self.replanFile = '/home/marie/project_thesis/Planning/p_replan.pddl'
        self.makeProblemFile()

        self.plan       = Planner(self.planner, self.algorithm, self.scenario, replan=True)

    def makeProblemFile(self):
        f   = open(self.replanFile, "w")
        _, problemFile = getDomainProblemFiles(self.planner, replan=False, scenario=self.scenario)
        fPF = open(problemFile, "r")

        if self.planner == PlannerType.TEMPORAL:
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
        for state in self.init:
            if "=" in state:
                initLines.append("        " + state + "\n")
            elif "intransit" in state:
                # If a vessel is intransit, we simplify and say that
                # the vessel is at the port it was transitting from
                state = state.replace("intransit", "vesselat")
                initLines.append("        (" + state + ")\n")
            elif self.scenario == 2 and "chargeteamat chargeteam0 portd" in state:
                ...
            else:
                initLines.append("        (" + state + ")\n")
        if self.lowBattery:
            initLines.append("        (chargeteamat chargeteam0 port" + self.port0.lower() + ")\n")
        initLines.append("    )\n")
        initLines.append("\n")

        goalLines       = ["    (:goal (and\n"]
        if self.lowBattery:
            goalLines.append("        (fullbattery battery0)\n")

        for state in self.goal:
            goalLines.append("        (" + state + ")\n")
        goalLines.append("    ))\n")
        goalLines.append("\n")

        if self.planner == PlannerType.TEMPORAL:
            endLines = ["    (:metric minimize (total-time))\n", ")\n"]
        else:
            endLines = [")\n"]

        lines = firstLine + objectLines + initLines + goalLines + endLines

        for line in lines:
            f.write(line)
        f.close()