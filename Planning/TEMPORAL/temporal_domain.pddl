(define (domain temporal)
(:requirements :typing :durative-actions :fluents)
    (:types
        vessel
        port
        goods
        tank
        fuelteam
    )

    (:predicates
        (vesselat ?v - vessel ?p - port)
        (goodsat ?g - goods ?p - port)
        (fuelteamat ?f - fuelteam ?p - port)
        (onboard ?g - goods ?v - vessel)
        (path ?x - port ?y - port)
        (isdocked ?v - vessel)
        (fulltank ?t - tank)
        (intransit ?v - vessel ?from - port)
        (isloading ?v - vessel)
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
            (at start (not (vesselat ?v ?from)))
            (at start (intransit ?v ?from))
        	(at end (vesselat ?v ?to))
            (at end (not (intransit ?v ?from)))
        )
    )

    (:durative-action dock
        :parameters (?p - port ?v - vessel)
        :duration (= ?duration 10)
        :condition (and
            (at start ( not (isdocked ?v)))
            (at start (vesselat ?v ?p))
        )
        :effect (and
            (at end (isdocked ?v))
        )
    )

    (:durative-action undock
        :parameters (?p - port ?v - vessel)
        :duration (= ?duration 10)
        :condition (and
            (at start (isdocked ?v))
            (at start (vesselat ?v ?p))
        )
        :effect (and
            (at start (not (isdocked ?v)))
        )
    )

    (:durative-action load
        :parameters (?p - port ?v - vessel ?g - goods)
        :duration (= ?duration 60)
        :condition (and
            (at start (vesselat ?v ?p))
            (at start (isdocked ?v))
            (at start (goodsat ?g ?p))
            ;(at start (not (isloading ?v)))
        )
        :effect (and
            (at start (not (goodsat ?g ?p)))
            ;(at start (isloading ?v))
            (at end (onboard ?g ?v))
            ;(at end (not (isloading ?v)))
        )
    )

    (:durative-action unload
        :parameters (?p - port ?v - vessel ?g - goods)
        :duration (= ?duration 50)
        :condition (and
            (at start (vesselat ?v ?p))
            (at start (isdocked ?v))
            (at start (onboard ?g ?v))
            ;(at start (not (isloading ?v)))
        )
        :effect (and
            (at start (not (onboard ?g ?v)))
            ;(at start (isloading ?v))
            (at end (goodsat ?g ?p))
            ;(at end (not (isloading ?v)))
        )
    )

    (:durative-action fuelling
        :parameters (?p - port ?v - vessel ?t - tank ?f - fuelteam)
        :duration (= ?duration 50)
        :condition (and
            (at start (vesselat ?v ?p))
            (at start (isdocked ?v))
            (at start (fuelteamat ?f ?p))
        )
        :effect (and
            (at end (fulltank ?t))
        )
    )

)
