(define (problem simple) (:domain simple)
    (:objects
        vessel0 - vessel
        porta portb portc portd porte - port
        goodsab goodsce goodscd - goods
    )

    (:init
        (vesselat vessel0 porta)
        (path porta portb)
        (path portb portc)
        (path portc portd)
        (path portd porte)
        (goodsat goodsab porta)
        (goodsat goodsce portc)
    )

    (:goal (and
        (vesselat vessel0 porte)
        (goodsat goodsab portb)
        (goodsat goodsce porte)
    ))
)