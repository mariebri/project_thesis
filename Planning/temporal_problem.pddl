(define (problem temporal) (:domain temporal)
    (:objects
        vessel0 - vessel
        porta portb portc portd porte - port
        goodsab goodsce goodscd - goods
        tank0 - tank
        fuelteam0 - fuelteam
    )

    (:init
        (vesselat vessel0 porta)
        (isdocked vessel0)
        (empty tank0)
        (fuelteamat fuelteam0 portc)
        (path porta portb)
        (path portb portc)
        (path portc portd)
        (path portd porte)
        (goodsat goodsab porta)
        (goodsat goodsce portc)
        (goodsat goodscd portc)
        (= (length porta portb) 5000)   ; m
        (= (length portb portc) 2500)   ; m
        (= (length portc portd) 3000)   ; m
        (= (length portd porte) 1500)   ; m
        (= (speed vessel0) 3)           ; m/s (approx 6 knots)
    )

    (:goal (and
        (vesselat vessel0 porte)
        (isdocked vessel0)
        (goodsat goodsab portb)
        (goodsat goodsce porte)
        (goodsat goodscd portd)
        (full tank0)
    ))

    (:metric minimize (total-time))
)
