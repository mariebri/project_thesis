(define (domain simple_graphplan)
    (:requirements :typing :strips)
    (:types
        vessel
        port
    )

    (:predicates
        (at ?v - vessel ?p - port)
        (path ?x - port ?y - port)
    )

    (:action move
        :parameters (?from - port ?to - port ?v - vessel)
        :precondition (and (path ?from ?to) (at ?v ?from))
        :effect (and (at ?v ?to) (not (at ?v ?from)))
    )
)