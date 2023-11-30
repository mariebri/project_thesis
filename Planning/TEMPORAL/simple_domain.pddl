(define (domain simple_temporal)
(:requirements :typing :durative-actions)
    (:types
        vessel
        port
        goods
    )

    (:predicates
        (vesselAt ?v - vessel ?p - port)
        (goodsAt ?g - goods ?p - port)
        (onboard ?g - goods ?v - vessel)
        (isDocked ?v - vessel)
    )

    (:functions
        (length ?x ?y - port)
        (speed ?v - vessel)
    )

    (:durative-action transit
        :parameters (?from ?to - port ?v - vessel)
        :duration (= ?duration (/ (length ?from ?to) (speed ?v)))
        :condition (and
        	(at start (vesselAt ?v ?from))
        )
        :effect (and
        	(at end (vesselAt ?v ?to))
        	(at start (not (vesselAt ?v ?from)))
        )
    )

    (:durative-action load
        :parameters (?p - port ?g - goods ?v - vessel)
        :duration (= ?duration 60)
        :condition (and
        	(at start (goodsAt ?g ?p))
        	(over all (vesselAt ?v ?p))
            (over all (isDocked ?v))
        )
        :effect (and 
        	(at end (not (goodsAt ?g ?p)))
        	(at end (onboard ?g ?v))
        )
    )

    (:durative-action unload
        :parameters (?p - port ?g - goods ?v - vessel)
        :duration (= ?duration 50)
        :condition (and
        	(at start (onboard ?g ?v))
        	(over all (vesselAt ?v ?p))
            (over all (isDocked ?v))
        )
        :effect (and
        	(at end (not (onboard ?g ?v)))
        	(at end (goodsAt ?g ?p))
        )
    )
)
