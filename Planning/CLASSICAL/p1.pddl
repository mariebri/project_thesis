(define (problem graphplan) (:domain graphplan)
    (:objects
        vessel0 - vessel
        cont0 cont1 cont2 - cont
        charger0 - charger
        battery0 - battery
        porta portb portc portd porte - port
        path_ab path_bc path_cb path_be path_eb path_cd path_dc path_ce path_ec - path
    )

    (:init
        (at vessel0 porta)
        (isdocked vessel0)
        (at charger0 portd)
        (at cont0 porta)
        (at cont1 portb)
        (at cont2 portc)
        (connected path_ab porta portb)
        (connected path_bc portb portc)
        (connected path_cb portc portb)
        (connected path_be portb porte)
        (connected path_eb porte portb)
        (connected path_cd portc portd)
        (connected path_dc portd portc)
        (connected path_ce portc porte)
        (connected path_ec porte portc)
    )

    (:goal (and
        (at cont0 porte)
        (at cont1 portd)
        (at cont2 portb)
        (fullbattery battery0)
    ))
)