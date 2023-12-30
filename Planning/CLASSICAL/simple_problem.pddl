(define (problem simple) (:domain simple)
    (:objects
        vessel0 - vessel
        porta portb - port
        goodsab - goods
    )

    (:init
        (vesselat vessel0 porta)
        (goodsat goodsab porta)
    )

    (:goal (and
        (vesselat vessel0 portb)
        (goodsat goodsab portb)
    ))
)
