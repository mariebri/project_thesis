import casadi as ca
import numpy as np
import dubins

from enum import Enum
from revolt import ReVolt

PlannerType = Enum('PlannerType', ['TEMPORAL', 'GRAPHPLAN'])
State       = Enum('State', ['DOCKED', 'DOCKING', 'UNDOCKING', 'IN_TRANSIT'])

def getDomainProblemFiles(plannerType: PlannerType, scenario=1, replan=False):
    if plannerType == PlannerType.TEMPORAL:
        domainFile  = "/home/marie/project_thesis/Planning/TEMPORAL/domain.pddl"
        problemFile = "/home/marie/project_thesis/Planning/TEMPORAL/p" + str(scenario) + ".pddl"

    elif plannerType == PlannerType.GRAPHPLAN:
        domainFile  = "/home/marie/project_thesis/Planning/CLASSICAL/domain.pddl"
        problemFile = "/home/marie/project_thesis/Planning/CLASSICAL/p" + str(scenario) + ".pddl"

    if replan:
        problemFile = "/home/marie/project_thesis/Planning/p_replan.pddl"

    return domainFile, problemFile

def getPortName(portFrom: str, portTo="", state=State.IN_TRANSIT):
    portFrom    = (portFrom.strip('-port')).upper()
    if portTo != "":
        portTo      = (portTo.strip('port')).upper()
    
    if state == State.DOCKING:
        portTo      = portFrom + "-port"
    elif state == State.UNDOCKING:
        portTo      = portFrom
        portFrom    = portTo + "-port"
    
    return portFrom, portTo

def ssa(angle):
    return ca.fmod(angle + ca.pi, 2*ca.pi) - ca.pi

def saturate(x, xMin, xMax):
    if x > xMax:
        x = xMax
    elif x < xMin:
        x = xMin
    return x

def dubinsPath(eta_start, eta_end, curvature=1.0, step=10):
    """
    Source: https://github.com/AndrewWalker/pydubins/tree/master
    Goal: Find shortest paths between two points
    Returns: The desired poses
    """
    path        = dubins.shortest_path(eta_start, eta_end, curvature)
    eta_d, _    = path.sample_many(step)

    # Make eta_d a 3xN matrix
    eta         = np.zeros((3, len(eta_d)))  
    for i in range(len(eta_d)):
        e       = eta_d[i]
        eta[0,i]= e[0]
        eta[1,i]= e[1]
        eta[2,i]= ssa(e[2])
    
    return eta
