(define (problem replan) (:domain temporal)
    (:objects
        vessel0 - vessel
        cont0 cont1 - cont
        charger0 - charger
        battery0 - battery
        porta portb portc portd porte - port
        path_ab path_bc path_cb path_be path_eb path_cd path_dc path_ce path_ec - path
    )

    (:init
        (connected path_ab porta portb)
        (connected path_bc portb portc)
        (connected path_cb portc portb)
        (connected path_be portb porte)
        (connected path_eb porte portb)
        (connected path_cd portc portd)
        (connected path_dc portd portc)
        (connected path_ce portc porte)
        (connected path_ec porte portc)
        (= (length path_ab) 587)
        (= (length path_bc) 758)
        (= (length path_cb) 758)
        (= (length path_be) 831)
        (= (length path_eb) 831)
        (= (length path_cd) 438)
        (= (length path_dc) 438)
        (= (length path_ce) 685)
        (= (length path_ec) 685)
        (= (speed vessel0) 1.2)
        (at charger0 portc)
        (onboard cont0 vessel0)
        (onboard cont1 vessel0)
        (at vessel0 portd)
        (isdocked vessel0)
    )

    (:goal (and
        (at cont0 porte)
        (at cont1 portd)
        (fullbattery battery0)
    ))

    (:metric minimize (total-time))
)
