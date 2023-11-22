(define (problem replan) (:domain graphplan)
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
        (fuelteamat fuelteam0 portb)
        (truckat trucka porta)
        (truckat truckb portb)
        (truckat truckc portc)
        (truckat truckd portd)
        (truckat trucke porte)
        (truckfree truckc)
        (truckfree truckd)
        (truckfree trucke)
        (goodsat goodsbd portb)
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
        (truckfree trucka)
        (vesselat vessel0 portb)
        (isdocked vessel0)
        (goodsat goodsab portb)
        (truckfree truckb)
    )

    (:goal (and
        (goodsat goodsce porte)
        (full tank0)
    ))

)
