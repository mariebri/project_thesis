(define (domain graphplan)
    (:requirements :typing)
    (:types
        vessel cont charger - object
        battery
        port
        path
    )

    (:predicates
        (at ?o - object ?p - port)
        (onboard ?c - cont ?v - vessel)
        (connected ?p - path ?x ?y - port)
        (isdocked ?v - vessel)
        (fullbattery ?b - battery)
    )

    (:action transit
        :parameters (?from ?to - port ?v - vessel ?p - path)
        :precondition (and
            (connected ?p ?from ?to)
            (at ?v ?from)
            (not (isdocked ?v))
        )
        :effect (and
            (at ?v ?to)
            (not (at ?v ?from))
        )
    )

    (:action dock
        :parameters (?p - port ?v - vessel)
        :precondition (and
            (not (isdocked ?v))
            (at ?v ?p)
        )
        :effect (and
            (isdocked ?v)
        )
    )

    (:action undock
        :parameters (?p - port ?v - vessel)
        :precondition (and
            (isdocked ?v)
            (at ?v ?p)
        )
        :effect (and
            (not (isdocked ?v))
        )
    )

    (:action load
        :parameters (?p - port ?c - cont ?v - vessel)
        :precondition (and
            (at ?c ?p)
            (at ?v ?p)
            (isdocked ?v)
        )
        :effect (and
            (not (at ?c ?p))
            (onboard ?c ?v)
        )
    )

    (:action unload
        :parameters (?p - port ?c - cont ?v - vessel)
        :precondition (and
            (onboard ?c ?v)
            (at ?v ?p)
            (isdocked ?v)
        )
        :effect (and
            (not (onboard ?c ?v))
            (at ?c ?p)
        )
    )

    (:action charging
        :parameters (?p - port ?v - vessel ?b - battery ?ch - charger)
        :precondition (and
            (at ?ch ?p)
            (at ?v ?p)
            (isdocked ?v)
        )
        :effect (and
            (fullbattery ?b)
        )
    )
)