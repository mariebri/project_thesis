(define (domain simple)
    (:requirements :typing :strips)
    (:types
        vessel cont - object
        port
    )

    (:predicates
        (at ?o - object ?p - port)
        (onboard ?c - cont ?v - vessel)
    )

    (:action transit
        :parameters (?from ?to - port ?v - vessel)
        :precondition (and (at ?v ?from))
        :effect (and
            (at ?v ?to)
            (not (at ?v ?from))
        )
    )

    (:action load
        :parameters (?p - port ?c - cont ?v - vessel)
        :precondition (and (at ?c ?p) (at ?v ?p))
        :effect (and
            (not (at ?c ?p))
            (onboard ?c ?v)
        )
    )

    (:action unload
        :parameters (?p - port ?c - cont ?v - vessel)
        :precondition (and (onboard ?c ?v) (at ?v ?p))
        :effect (and
            (not (onboard ?c ?v))
            (at ?c ?p)
        )
    )
)
