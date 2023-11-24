(define (problem temporal) (:domain temporal)
    (:objects
        vessel0 - vessel
        porta portb portc portd porte - port
        goodsae goodsbd - goods
        tank0 - tank
        fuelteam0 - fuelteam
    )

    (:init
        (vesselat vessel0 porta)
        (isdocked vessel0)
        (fuelteamat fuelteam0 portb)
        (goodsat goodsae porta)
        (goodsat goodsbd portb)
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
        (= (speed vessel0) 3)          ; m/s (approx 6 knots)
    )

    (:goal (and
        (goodsat goodsae porte)
        (goodsat goodsbd portd)
        (fulltank tank0)
    ))

    (:metric minimize (total-time))
)
