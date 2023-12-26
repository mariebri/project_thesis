(define (problem temporal) (:domain simple_temporal)
    (:objects
        vessel0 - vessel
        portA portB - port
        goods0 - goods
    )

    (:init
        (vesselAt vessel0 portA)
        (goodsAt goods0 portA)
        (= (length portA portB) 2000)    ; m
        (= (speed vessel0) 5)            ; m/s
    )

    (:goal (and
        (goodsAt goods0 portB)
    ))

    (:metric minimize (total-time))
)
