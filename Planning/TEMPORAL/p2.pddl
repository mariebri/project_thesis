(define (problem temporal) (:domain temporal)
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
        (= (length porta portb) 587)   ; m
        (= (length portb porta) 587)   ; m
        (= (length portb portc) 758)   ; m
        (= (length portc portb) 758)   ; m
        (= (length portb porte) 831)   ; m
        (= (length porte portb) 831)   ; m
        (= (length portc portd) 438)   ; m
        (= (length portd portc) 438)   ; m
        (= (length portc porte) 685)   ; m
        (= (length porte portc) 685)   ; m
        (= (speed vessel0) 1.4)        ; m/s
        (chargerat charger0 portc)
        (chargerat charger0 portd)
    )

    (:goal (and
        (contat cont0 porte)
        (contat cont1 portd)
        (fullbattery battery0)
    ))

    (:metric minimize (total-time))
)
