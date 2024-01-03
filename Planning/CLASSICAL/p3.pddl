(define (problem graphplan) (:domain graphplan)
    (:objects
        vessel0 - vessel
        porta portb portc portd porte - port
        cont0 cont1 - cont
        battery0 - battery
        charger0 - charger
    )

    (:init
        (vesselat vessel0 porta)
        (isdocked vessel0)
        (contat cont0 porta)
        (contat cont1 portb)
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
        (contat cont0 porte)
        (contat cont1 portd)
    ))
)