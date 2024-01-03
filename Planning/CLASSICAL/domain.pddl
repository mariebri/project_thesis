(define (domain graphplan)
    (:requirements :typing)
    (:types
        vessel
        port
        cont
        battery
        charger
    )

    (:predicates
        (vesselat ?v - vessel ?p - port)
        (contat ?c - cont ?p - port)
        (chargerat ?ch - charger ?p - port)
        (onboard ?c - cont ?v - vessel)
        (path ?x - port ?y - port)
        (isdocked ?v - vessel)
        (fullbattery ?b - battery)
    )

    (:action transit
        :parameters (?from - port ?to - port ?v - vessel)
        :precondition (and
            (path ?from ?to)
            (vesselat ?v ?from)
            (not (isdocked ?v))
        )
        :effect (and
            (vesselat ?v ?to)
            (not (vesselat ?v ?from))
        )
    )

    (:action dock
        :parameters (?p - port ?v - vessel)
        :precondition (and
            (not (isdocked ?v))
            (vesselat ?v ?p)
        )
        :effect (and
            (isdocked ?v)
        )
    )

    (:action undock
        :parameters (?p - port ?v - vessel)
        :precondition (and
            (isdocked ?v)
            (vesselat ?v ?p)
        )
        :effect (and
            (not (isdocked ?v))
        )
    )

    (:action load
        :parameters (?p - port ?c - cont ?v - vessel)
        :precondition (and
            (contat ?c ?p)
            (vesselat ?v ?p)
            (isdocked ?v)
        )
        :effect (and
            (not (contat ?c ?p))
            (onboard ?c ?v)
        )
    )

    (:action unload
        :parameters (?p - port ?c - cont ?v - vessel)
        :precondition (and
            (onboard ?c ?v)
            (vesselat ?v ?p)
            (isdocked ?v)
        )
        :effect (and
            (not (onboard ?c ?v))
            (contat ?c ?p)
        )
    )

    (:action charging
        :parameters (?p - port ?v - vessel ?b - battery ?ch - charger)
        :precondition (and
            (chargerat ?ch ?p)
            (vesselat ?v ?p)
            (isdocked ?v)
        )
        :effect (and
            (fullbattery ?b)
        )
    )
)