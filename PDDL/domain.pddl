(define (domain ca4_test)
    (:requirements :typing :durative-actions :fluents)
    (:types
        valve pump - checkobj
        valve pump charger robot - atobj    ; At object
        battery camera - onbobj             ; Onboard object
        robot battery camera charger pump valve waypoint
    )

    (:predicates
        (at ?obj - atobj ?wp - waypoint)
        (onboard ?obj - onbobj ?r - robot)
        (no-check ?obj - checkobj)
        (check ?obj - checkobj)
        (no-bat ?b - battery)
        (full-bat ?b - battery)
        (path ?x - waypoint ?y - waypoint)
    )

    (:functions
        (totalTime)
    )

    (:durative-action move
        :parameters (?from - waypoint ?to - waypoint ?r - robot ?b - battery)
        :duration (= ?duration 5)
        :condition ( and (at start (at ?r ?from)) (over all (path ?from ?to)) (at start (full-bat ?b)))
        :effect ( and (at end (at ?r ?to)) (at end (not (at ?r ?from))) (at start (increase (totalTime) 5)) )
    )

    (:durative-action take-picture
        :parameters (?wp - waypoint ?p - pump ?r - robot ?c - camera)
        :duration (= ?duration 1)
        :condition ( and (over all (onboard ?c ?r)) (over all (at ?p ?wp)) (over all (at ?r ?wp)) (at start (no-check ?p)) )
        :effect ( and (at end (check ?p)) (at end (not (no-check ?p))) (at start (increase (totalTime) 1)) )
    )

    (:durative-action inspect-valve
        :parameters (?wp - waypoint ?v - valve ?r - robot)
        :duration (= ?duration 1)
        :condition ( and (over all (at ?v ?wp)) (over all (at ?r ?wp)) (at start (no-check ?v)) )
        :effect ( and (at end (check ?v)) (at end (not (no-check ?v))) (at start (increase (totalTime) 1)) )
    )

    (:durative-action charge-robot
        :parameters (?wp - waypoint ?c - charger ?r - robot ?b - battery)
        :duration (= ?duration 10)
        :condition ( and (over all (onboard ?b ?r)) (over all (at ?r ?wp)) (over all (at ?c ?wp)) (at start (no-bat ?b)))
        :effect ( and (at end (full-bat ?b)) (at end (not (no-bat ?b))) (at start (increase (totalTime) 10)) )
    )
)