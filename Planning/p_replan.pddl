(define (problem replan) (:domain graphplan)
    (:objects
        vessel0 - vessel
        porta portb portc portd porte - port
        goodsae goodsbd - goods
        tank0 - tank
        chargeteam0 - chargeteam
    )

    (:init
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
        (onboard goodsae vessel0)
        (vesselat vessel0 portb)
        (onboard goodsbd vessel0)
        (chargeteamat chargeteam0 porte)
    )

    (:goal (and
        (fulltank tank0)
        (goodsat goodsae porte)
        (goodsat goodsbd portd)
    ))

)
