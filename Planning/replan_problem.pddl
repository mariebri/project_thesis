(define (problem replan) (:domain temporal)
    (:objects
        vessel0 - vessel
        porta portb portc portd porte - port
        goodsab goodsce goodscd - goods
        tank0 - tank
        fuelteam0 - fuelteam
    )

    (:init
        (empty tank0)
        (fuelteamat fuelteam0 portb)
        (path porta portb)
        (path portb portc)
        (path portc portd)
        (path portd porte)
        (goodsat goodsce portc)
        (goodsat goodscd portc)
        (= (length porta portb) 5000)
        (= (length portb portc) 2500)
        (= (length portc portd) 3000)
        (= (length portd porte) 1500)
        (= (speed vessel0) 3)
        (onboard goodsab vessel0)
        (vesselat vessel0 portb)
        (isdocked vessel0)
    )

    (:goal (and
        (vesselat vessel0 porte)
        (goodsat goodsab portb)
        (goodsat goodsce porte)
        (goodsat goodscd portd)
        (full tank0)
    ))

    (:metric minimize (total-time))
)
