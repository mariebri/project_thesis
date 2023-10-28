(define (problem temporal) (:domain simple_temporal)
    (:objects
        vessel0 - vessel
        portA portB portC portD portE - port
        goodsAB goodsCE - goods
    )

    (:init
        (at vessel0 portA)
        (path portA portB) (path portB portC) (path portC portD) (path portD portE)
        (goodsAt goodsAB portA) (goodsAt goodsCE portC)
        (= (length portA portB) 25)
        (= (length portB portC) 20)
        (= (length portC portD) 35)
        (= (length portD portE) 15)
    )

    (:goal (and
        (at vessel0 portE) (goodsAt goodsAB portB) (goodsAt goodsCE portE)
    ))

    (:metric minimize (total-time))
)
