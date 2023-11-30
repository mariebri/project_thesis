(define (problem graphplan) (:domain graphplan)
    (:objects
        vessel0 - vessel
        porta portb portc portd porte - port
        goodsae goodsbd goodscb - goods
        tank0 - tank
        fuelteam0 - fuelteam
    )

    (:init
        (vesselat vessel0 porta)
        (isdocked vessel0)
        (fuelteamat fuelteam0 portd)
        (goodsat goodsae porta)
        (goodsat goodsbd portb)
        (goodsat goodscb portc)
        (path porta portb)
        (path portb porta)
        (path portb portc)
        (path portc portb)
        (path portb porte)
        (path porte portb)
        (path portc portd)
        (path portd portc)
        (path portc porte)
        (path porte portc)
    )

    (:goal (and
        (goodsat goodsae porte)
        (goodsat goodsbd portd)
        (goodsat goodscb portb)
        (fulltank tank0)
    ))
)