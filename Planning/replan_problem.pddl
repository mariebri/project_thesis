(define (problem replan) (:domain temporal)
    (:objects
        vessel0 - vessel
        porta portb portc portd porte - port
        goodsae goodsbd - goods
        tank0 - tank
        fuelteam0 - fuelteam
    )

    (:init
        (fuelteamat fuelteam0 portd)
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
        (= (length porta portb) 587)
        (= (length portb porta) 587)
        (= (length portb portc) 758)
        (= (length portc portb) 758)
        (= (length portb porte) 831)
        (= (length porte portb) 831)
        (= (length portc portd) 438)
        (= (length portd portc) 438)
        (= (length portc porte) 685)
        (= (length porte portc) 685)
        (= (speed vessel0) 3)
        (fuelteamat fuelteam0 porta)
        (fuelteamat fuelteam0 portb)
        (fuelteamat fuelteam0 portc)
        (fuelteamat fuelteam0 porte)
        (onboard goodsae vessel0)
        (onboard goodsbd vessel0)
        (vesselat vessel0 portd)
        (isdocked vessel0)
    )

    (:goal (and
        (fulltank tank0)
    ))

    (:metric minimize (total-time))
)
