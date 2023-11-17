(define (domain temporal)
(:requirements :typing :durative-actions :fluents)
    (:types
        vessel
        port
        goods
    )

    (:predicates
        (vesselAt ?v - vessel ?p - port)
        (goodsAt ?g - goods ?p - port)
        (fuelAt ?p - port)
        (onboard ?g - goods ?v - vessel)
        (path ?x - port ?y - port)
        (isDocked ?v - vessel)
        (hasFueled ?v - vessel)
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
        	(over all (path ?from ?to))
            (over all (not (isDocked ?v)))
            ; (at start (> (battery ?v) 25))
        )
        :effect (and
        	(at end (vesselAt ?v ?to))
        	(at start (not (vesselAt ?v ?from)))
            ; (at end (- (battery ?v) 20))
        )
    )

    (:durative-action undock
        :parameters (?p - port ?v - vessel)
        :duration (= ?duration 10)
        :condition (and
            (at start (isDocked ?v))
            (over all (vesselAt ?v ?p))
        )
        :effect (and
            (at end (not (isDocked ?v)))
        )
    )

    (:durative-action dock
        :parameters (?p - port ?v - vessel)
        :duration (= ?duration 10)
        :condition (and
            (at start ( not (isDocked ?v)))
            (over all (vesselAt ?v ?p))
        )
        :effect (and
            (at end (isDocked ?v))
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
        	(at start (not (goodsAt ?g ?p)))
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
        	(at start (not (onboard ?g ?v)))
        	(at end (goodsAt ?g ?p))
        )
    )

    (:durative-action fuelling
        :parameters (?p - port ?v - vessel)
        :duration (= ?duration 50)
        :condition (and
            (at start (fuelAt ?p))
            (at start (not (hasFueled ?v)))
            (over all (vesselAt ?v ?p))
            (over all (isDocked ?v))
        )
        :effect (and
            (at end (hasFueled ?v))
        )
    )

)
