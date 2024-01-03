(define (domain simple_temporal)
(:requirements :typing :durative-actions)
    (:types
        vessel cont - object
        port
    )

    (:predicates
        (at ?o - object ?p - port)
        (onboard ?c - cont ?v - vessel)
    )

    (:functions
        (length ?x ?y - port)
        (speed ?v - vessel)
    )

    (:durative-action move
        :parameters (?from ?to - port ?v - vessel)
        :duration (= ?duration (/ (length ?from ?to) (speed ?v)))
        :condition (and
        	(at start (at ?v ?from))
        )
        :effect (and
        	(at end (at ?v ?to))
        	(at start (not (at ?v ?from)))
        )
    )

    (:durative-action load
        :parameters (?p - port ?c - cont ?v - vessel)
        :duration (= ?duration 60)
        :condition (and
        	(at start (at ?c ?p))
        	(over all (at ?v ?p))
        )
        :effect (and 
        	(at end (not (at ?c ?p)))
        	(at end (onboard ?c ?v))
        )
    )

    (:durative-action unload
        :parameters (?p - port ?c - cont ?v - vessel)
        :duration (= ?duration 50)
        :condition (and
        	(at start (onboard ?c ?v))
        	(over all (at ?v ?p))
        )
        :effect (and
        	(at end (not (onboard ?c ?v)))
        	(at end (at ?c ?p))
        )
    )
)
