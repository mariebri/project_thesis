(define (domain temporal)
(:requirements :typing :durative-actions :fluents)
    (:types
        vessel
        port
        goods
        battery
        chargeteam
    )

    (:predicates
        (vesselat ?v - vessel ?p - port)
        (goodsat ?g - goods ?p - port)
        (chargeteamat ?c - chargeteam ?p - port)
        (onboard ?g - goods ?v - vessel)
        (path ?x - port ?y - port)
        (isdocked ?v - vessel)
        (fullbattery ?b - battery)
        (intransit ?v - vessel ?from - port)
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
            (at start (isdocked ?v))
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
        :parameters (?p - port ?g - goods ?v - vessel)
        :duration (= ?duration 60)
        :condition (and
            (at start (vesselat ?v ?p))
            (at start (isdocked ?v))
            (at start (goodsat ?g ?p))
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
            (at start (vesselat ?v ?p))
            (at start (isdocked ?v))
            (at start (onboard ?g ?v))
        )
        :effect (and
            (at start (not (onboard ?g ?v)))
            (at end (goodsat ?g ?p))
        )
    )

    (:durative-action charging
        :parameters (?p - port ?v - vessel ?b - battery ?c - chargeteam)
        :duration (= ?duration 50)
        :condition (and
            (at start (vesselat ?v ?p))
            (at start (isdocked ?v))
            (at start (chargeteamat ?c ?p))
        )
        :effect (and
            (at end (fullbattery ?b))
        )
    )

)
