(define (problem temporal) (:domain temporal)
    (:objects
        vessel0 - vessel
        portA portB portC portD portE - port
        goodsAB goodsCE - goods
    )

    (:init
        (vesselAt vessel0 portA) (isDocked vessel0)
        (path portA portB) (path portB portC) (path portC portD) (path portD portE)
        (goodsAt goodsAB portA) (goodsAt goodsCE portC)
        (= (length portA portB) 5000)   ; m
        (= (length portB portC) 2500)   ; m
        (= (length portC portD) 3000)   ; m
        (= (length portD portE) 1500)   ; m
        (= (speed vessel0) 20)          ; m/s
        ; (= (battery vessel0) 100)       ; battery percentage %
    )

    (:goal (and
        (vesselAt vessel0 portE) (isDocked vessel0) (goodsAt goodsAB portB) (goodsAt goodsCE portE)
    ))

    (:metric minimize (total-time))
)
