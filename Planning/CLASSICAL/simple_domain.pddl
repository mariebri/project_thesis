(define (domain simple)
    (:requirements :typing :strips)
    (:types
        vessel
        port
        cont
    )

    (:predicates
        (vesselAt ?v - vessel ?p - port)
        (contAt ?c - cont ?p - port)
        (onboard ?c - cont ?v - vessel)
    )

    (:action transit
        :parameters (?from ?to - port ?v - vessel)
        :precondition (and (vesselAt ?v ?from))
        :effect (and
            (vesselAt ?v ?to)
            (not (vesselAt ?v ?from))
        )
    )

    (:action load
        :parameters (?p - port ?c - cont ?v - vessel)
        :precondition (and (contAt ?c ?p) (vesselAt ?v ?p))
        :effect (and
            (not (contAt ?c ?p))
            (onboard ?c ?v)
        )
    )

    (:action unload
        :parameters (?p - port ?c - cont ?v - vessel)
        :precondition (and (onboard ?c ?v) (vesselAt ?v ?p))
        :effect (and
            (not (onboard ?c ?v))
            (contAt ?c ?p)
        )
    )
)
