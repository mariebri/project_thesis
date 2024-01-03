(define (domain simple_temporal)
(:requirements :typing :durative-actions)
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

    (:functions
        (length ?x ?y - port)
        (speed ?v - vessel)
    )

    (:durative-action move
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
        :parameters (?p - port ?c - cont ?v - vessel)
        :duration (= ?duration 60)
        :condition (and
        	(at start (contAt ?c ?p))
        	(over all (vesselAt ?v ?p))
        )
        :effect (and 
        	(at end (not (contAt ?c ?p)))
        	(at end (onboard ?c ?v))
        )
    )

    (:durative-action unload
        :parameters (?p - port ?c - cont ?v - vessel)
        :duration (= ?duration 50)
        :condition (and
        	(at start (onboard ?c ?v))
        	(over all (vesselAt ?v ?p))
        )
        :effect (and
        	(at end (not (onboard ?c ?v)))
        	(at end (contAt ?c ?p))
        )
    )
)
