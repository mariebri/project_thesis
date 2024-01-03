(define (problem graphplan) (:domain graphplan)
    (:objects
        vessel0 - vessel
        porta portb portc portd porte - port
        cont0 cont1 cont2 - cont
        battery0 - battery
        charger0 - charger
    )

    (:init
        (vesselat vessel0 porta)
        (isdocked vessel0)
        (chargerat charger0 portd)
        (contat cont0 porta)
        (contat cont1 portb)
        (contat cont2 portc)
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
        (contat cont2 portb)
        (fullbattery battery0)
    ))
)