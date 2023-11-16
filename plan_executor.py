### This module takes in a plan, and says which actions to perform
from planner import Plan, Action
import time


def executePlan(plan: Plan):
    actions = plan.actions

    for a in actions:
        executeAction(a)


def executeAction(a: Action):
    action  = a.getAction()
    pred    = a.getPredicates()
    start   = a.getStartTime()
    end     = a.getEndTime()
    dur     = a.getDuration()

    if action == "transit":
        # Transit - port_from; port_to; vessel
        portFrom    = pred[0]
        portTo      = pred[1]
        print("At %f" % start)
        print("Transit from %s to %s\n" % (portFrom, portTo))
        time.sleep(2)

    elif action == "undock":
        # Undock - port; vessel
        port = pred[0]
        print("At %f" % start)
        print("Undocking at %s\n" % port)
        time.sleep(2)

    elif action == "dock":
        # Dock - port; vessel
        port = pred[0]
        print("At %f" % start)
        print("Docking at %s\n" % port)
        time.sleep(2)

    elif action == "load":
        # Load - port; goods; vessel
        # Do nothing, be stationary for the duration
        port = pred[0]
        goods = pred[1]
        print("At %f" % start)
        print("Loading %s at %s\n" % (goods, port))
        time.sleep(2)

    elif action == "unload":
        # Unload - port; goods; vessel
        port = pred[0]
        goods = pred[1]
        print("At %f" % start)
        print("Unloading %s at %s\n" % (goods, port))
        time.sleep(2)

    elif action == "fuelling":
        # Fuelling - port; vessel
        port = pred[0]
        print("At %f" % start)
        print("Fuelling at %s\n" % port)
        time.sleep(2)

    else:
        raise Exception("Not a valid action name")