(define (problem replan) (:domain temporal)
    (:objects
        vessel0 - vessel
        porta portb portc portd porte - port
        goodsab goodsbd goodsce - goods
        tank0 - tank
        fuelteam0 - fuelteam
        trucka truckb truckc truckd trucke - truck
    )

    (:init
        (empty tank0)
        (fuelteamat fuelteam0 portc)
        (truckat trucka porta)
        (truckat truckb portb)
        (truckat truckc portc)
        (truckat truckd portd)
        (truckat trucke porte)
        (truckfree truckc)
        (truckfree truckd)
        (truckfree trucke)
        (goodsat goodsce portc)
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
        (truckfree trucka)
        (onboard goodsbd vessel0)
        (goodsat goodsab portb)
        (truckfree truckb)
        (vesselat vessel0 portc)
        (isdocked vessel0)
    )

    (:goal (and
        (goodsat goodsbd portd)
        (goodsat goodsce porte)
        (full tank0)
    ))

    (:metric minimize (total-time))
)
