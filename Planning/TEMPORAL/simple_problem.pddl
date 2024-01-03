(define (problem temporal) (:domain simple_temporal)
    (:objects
        vessel0 - vessel
        portA portB - port
        cont0 - cont
    )

    (:init
        (vesselAt vessel0 portA)
        (contAt cont0 portA)
        (= (length portA portB) 2000)    ; m
        (= (speed vessel0) 5)            ; m/s
    )

    (:goal (and
        (contAt cont0 portB)
    ))

    (:metric minimize (total-time))
)
