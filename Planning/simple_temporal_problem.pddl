(define (problem temporal) (:domain simple_temporal)
    (:objects
        vessel0 - vessel
        portA portB - port
        goods0 - goods
    )

    (:init
        (vesselAt vessel0 portA)
        (goodsAt goods0 portA)
        (= (length portA portB) 5000)   ; m
        (= (speed vessel0) 20)          ; m/s
    )

    (:goal (and
        (vesselAt vessel0 portB) (goodsAt goods0 portB)
    ))

    (:metric minimize (total-time))
)
