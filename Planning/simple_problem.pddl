(define (problem simple) (:domain simple_graphplan)
    (:objects
        vessel0 - vessel
        portA portB portC portD portE - port
        goodsAB goodsCE - goods
    )

    (:init
        (at vessel0 portA)
        (path portA portB) (path portB portC) (path portC portD) (path portD portE)
        (goodsAt goodsAB portA) (goodsAt goodsCE portC)
    )

    (:goal (and
        (at vessel0 portE) (goodsAt goodsAB portB) (goodsAt goodsCE portE)
    ))
)