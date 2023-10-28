(define (domain simple_temporal)
(:requirements :typing :durative-actions)
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

    (:functions
        (length ?x ?y - port)
    )

    (:durative-action move
        :parameters (?from ?to -port ?v - vessel)
        :duration (= ?duration (length ?from ?to))
        :condition (and
        	(at start (at ?v ?from))
        	(over all (path ?from ?to))
        )
        :effect (and
        	(at end (at ?v ?to))
        	(at start (not (at ?v ?from)))
        )
    )

    (:durative-action load
        :parameters (?p - port ?g - goods ?v - vessel)
        :duration (= ?duration 10)
        :condition (and
        	(at start (goodsAt ?g ?p))
        	(over all (at ?v ?p))
        )
        :effect (and 
        	(at end (not (goodsAt ?g ?p)))
        	(at end (onboard ?g ?v))
        )
    )

    (:durative-action unload
        :parameters (?p - port ?g - goods ?v - vessel)
        :duration (= ?duration 10)
        :condition (and
        	(at start (onboard ?g ?v))
        	(over all (at ?v ?p))
        )
        :effect (and
        	(at end (not (onboard ?g ?v)))
        	(at end (goodsAt ?g ?p))
        )
    )

)
