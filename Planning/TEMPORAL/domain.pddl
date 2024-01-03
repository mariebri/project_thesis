(define (domain temporal)
(:requirements :typing :durative-actions)
    (:types
        vessel cont charger - object
        battery
        port
        path
    )

    (:predicates
        (at ?o - object ?p - port)
        (onboard ?c - cont ?v - vessel)
        (connected ?p - path ?x ?y - port)
        (isdocked ?v - vessel)
        (fullbattery ?b - battery)
        (intransit ?v - vessel ?from - port)
    )

    (:functions
        (length ?p - path)
        (speed ?v - vessel)
    )

    (:durative-action transit
        :parameters (?from ?to - port ?v - vessel ?p - path)
        :duration (= ?duration (/ (length ?p) (speed ?v)))
        :condition (and
            (at start (at ?v ?from))
            (at start (connected ?p ?from ?to))
            (over all (not (isdocked ?v)))
        )
        :effect (and
            (at start (not (at ?v ?from)))
            (at start (intransit ?v ?from))
        	(at end (at ?v ?to))
            (at end (not (intransit ?v ?from)))
        )
    )

    (:durative-action dock
        :parameters (?p - port ?v - vessel)
        :duration (= ?duration 10)
        :condition (and
            (at start ( not (isdocked ?v)))
            (at start (at ?v ?p))
        )
        :effect (and
            (at start (isdocked ?v))
        )
    )

    (:durative-action undock
        :parameters (?p - port ?v - vessel)
        :duration (= ?duration 10)
        :condition (and
            (at start (isdocked ?v))
            (at start (at ?v ?p))
        )
        :effect (and
            (at start (not (isdocked ?v)))
        )
    )

    (:durative-action load
        :parameters (?p - port ?c - cont ?v - vessel)
        :duration (= ?duration 60)
        :condition (and
            (at start (at ?v ?p))
            (at start (isdocked ?v))
            (at start (at ?c ?p))
        )
        :effect (and
            (at start (not (at ?c ?p)))
            (at end (onboard ?c ?v))
        )
    )

    (:durative-action unload
        :parameters (?p - port ?c - cont ?v - vessel)
        :duration (= ?duration 50)
        :condition (and
            (at start (at ?v ?p))
            (at start (isdocked ?v))
            (at start (onboard ?c ?v))
        )
        :effect (and
            (at start (not (onboard ?c ?v)))
            (at end (at ?c ?p))
        )
    )

    (:durative-action charging
        :parameters (?p - port ?v - vessel ?b - battery ?ch - charger)
        :duration (= ?duration 50)
        :condition (and
            (at start (at ?v ?p))
            (at start (isdocked ?v))
            (at start (at ?ch ?p))
        )
        :effect (and
            (at end (fullbattery ?b))
        )
    )

)
