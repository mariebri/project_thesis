(define (problem replan) (:domain temporal)
    (:objects
        vessel0 - vessel
        porta portb portc portd porte - port
        goodsae goodsbd - goods
        tank0 - tank
        fuelteam0 - fuelteam
    )

    (:init
        (fuelteamat fuelteam0 portb)
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
        (onboard goodsae vessel0)
        (fulltank tank0)
        (goodsat goodsbd portd)
        (vesselat vessel0 portd)
    )

    (:goal (and
        (goodsat goodsae porte)
    ))

    (:metric minimize (total-time))
)
