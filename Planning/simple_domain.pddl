(define (domain simple)
    (:requirements :typing :strips)
    (:types
        vessel
        port
        goods
    )

    (:predicates
        (vesselat ?v - vessel ?p - port)
        (goodsat ?g - goods ?p - port)
        (onboard ?g - goods ?v - vessel)
        (path ?x - port ?y - port)
    )

    (:action transit
        :parameters (?from - port ?to - port ?v - vessel)
        :precondition (and (path ?from ?to) (vesselat ?v ?from))
        :effect (and
            (vesselat ?v ?to)
            (not (vesselat ?v ?from))
        )
    )

    (:action load
        :parameters (?p - port ?g - goods ?v - vessel)
        :precondition (and (goodsat ?g ?p) (vesselat ?v ?p))
        :effect (and
            (not (goodsat ?g ?p))
            (onboard ?g ?v)
        )
    )

    (:action unload
        :parameters (?p - port ?g - goods ?v - vessel)
        :precondition (and (onboard ?g ?v) (vesselat ?v ?p))
        :effect (and
            (not (onboard ?g ?v))
            (goodsat ?g ?p)
        )
    )
)