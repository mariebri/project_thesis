(define (domain temporal)
(:requirements :typing :durative-actions :fluents)
    (:types
        vessel
        port
        goods
        tank
    )

    (:predicates
        (vesselat ?v - vessel ?p - port)
        (goodsat ?g - goods ?p - port)
        (fuelat ?p - port)
        (onboard ?g - goods ?v - vessel)
        (path ?x - port ?y - port)
        (isdocked ?v - vessel)
        (empty ?t - tank)
        (full ?t - tank)
    )

    (:functions
        (length ?x ?y - port)
        (speed ?v - vessel)
    )

    (:durative-action transit
        :parameters (?from ?to - port ?v - vessel)
        :duration (= ?duration (/ (length ?from ?to) (speed ?v)))
        :condition (and
        	(at start (vesselat ?v ?from))
        	(over all (path ?from ?to))
            (over all (not (isdocked ?v)))
        )
        :effect (and
        	(at end (vesselat ?v ?to))
        	(at start (not (vesselat ?v ?from)))
        )
    )

    (:durative-action undock
        :parameters (?p - port ?v - vessel)
        :duration (= ?duration 10)
        :condition (and
            (at start (isdocked ?v))
            (over all (vesselat ?v ?p))
        )
        :effect (and
            (at end (not (isdocked ?v)))
        )
    )

    (:durative-action dock
        :parameters (?p - port ?v - vessel)
        :duration (= ?duration 10)
        :condition (and
            (at start ( not (isdocked ?v)))
            (over all (vesselat ?v ?p))
        )
        :effect (and
            (at end (isdocked ?v))
        )
    )

    (:durative-action load
        :parameters (?p - port ?g - goods ?v - vessel)
        :duration (= ?duration 60)
        :condition (and
        	(at start (goodsat ?g ?p))
        	(at start (vesselat ?v ?p))
            (over all (isdocked ?v))
        )
        :effect (and 
        	(at start (not (goodsat ?g ?p)))
        	(at end (onboard ?g ?v))
        )
    )

    (:durative-action unload
        :parameters (?p - port ?g - goods ?v - vessel)
        :duration (= ?duration 50)
        :condition (and
        	(at start (onboard ?g ?v))
        	(at start (vesselat ?v ?p))
            (over all (isdocked ?v))
        )
        :effect (and
        	(at start (not (onboard ?g ?v)))
        	(at end (goodsat ?g ?p))
        )
    )

    (:durative-action fuelling
        :parameters (?p - port ?v - vessel ?t - tank)
        :duration (= ?duration 50)
        :condition (and
            (at start (fuelat ?p))
            (at start (empty ?t))
            (at start (vesselat ?v ?p))
            (over all (isdocked ?v))
        )
        :effect (and
            (at end (full ?t))
        )
    )

)
