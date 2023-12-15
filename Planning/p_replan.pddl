(define (problem replan) (:domain temporal)
    (:objects
        vessel0 - vessel
        porta portb portc portd porte - port
        goodsae goodsbd goodscb - goods
        battery0 - battery
        chargeteam0 - chargeteam
    )

    (:init
        (chargeteamat chargeteam0 portd)
        (goodsat goodsbd portb)
        (goodsat goodscb portc)
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
        (= (speed vessel0) 1)
        (onboard goodsae vessel0)
        (vesselat vessel0 porta)
    )

    (:goal (and
        (goodsat goodsae porte)
        (goodsat goodsbd portd)
        (goodsat goodscb portb)
        (fullbattery battery0)
    ))

    (:metric minimize (total-time))
)
