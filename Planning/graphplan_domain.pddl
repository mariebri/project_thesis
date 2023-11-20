(define (domain graphplan)
    (:requirements :typing)
    (:types
        vessel
        port
        goods
    )

    (:predicates
        (vesselat ?v - vessel ?p - port)
        (goodsat ?g - goods ?p - port)
        (fuelteamat ?f - fuelteam ?p - port)
        (truckat ?t - truck ?p - port)
        (onboard ?g - goods ?v - vessel)
        (path ?x - port ?y - port)
        (isdocked ?v - vessel)
        (empty ?t - tank)
        (full ?t - tank)
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
        :parameters (?p - port ?g - goods ?v - vessel ?t - truck)
        :precondition (and
            (goodsat ?g ?p)
            (vesselat ?v ?p)
            (isdocked ?v)
            (truckat ?t ?p)
        )
        :effect (and
            (not (goodsat ?g ?p))
            (onboard ?g ?v)
        )
    )

    (:action unload
        :parameters (?p - port ?g - goods ?v - vessel ?t - truck)
        :precondition (and
            (onboard ?g ?v)
            (vesselat ?v ?p)
            (isdocked ?v)
            (truckat ?t ?p)
        )
        :effect (and
            (not (onboard ?g ?v))
            (goodsat ?g ?p)
        )
    )

    (:action fuelling
        :parameters (?p - port ?v - vessel ?t - tank ?f - fuelteam)
        :precondition (and
            (fuelteamat ?f ?p)
            (empty ?t)
            (vesselat ?v ?p)
            (isdocked ?v)
        )
        :effect (and
            (full ?t)
        )
    )
)