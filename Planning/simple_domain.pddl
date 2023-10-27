(define (domain simple_graphplan)
    (:requirements :typing :strips)
    (:types
        vessel
        port
        goods
    )

    (:predicates
        (at ?v - vessel ?p - port)
        (goodsAt ?g - goods ?p - port)
        (onboard ?g - goods ?v - vessel)
        (path ?x - port ?y - port)
    )

    (:action move
        :parameters (?from - port ?to - port ?v - vessel)
        :precondition (and (path ?from ?to) (at ?v ?from))
        :effect (and (at ?v ?to) (not (at ?v ?from)))
    )

    (:action load
        :parameters (?p - port ?g - goods ?v - vessel)
        :precondition (and (goodsAt ?g ?p) (at ?v ?p))
        :effect (and (not (goodsAt ?g ?p)) (onboard ?g ?v))
    )

    (:action unload
        :parameters (?p - port ?g - goods ?v - vessel)
        :precondition (and (onboard ?g ?v) (at ?v ?p))
        :effect (and (not (onboard ?g ?v)) (goodsAt ?g ?p))
    )
)