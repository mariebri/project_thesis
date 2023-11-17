(define (problem replan) (:domain temporal)
	(:objects
		vessel0 - vessel
		porta portb portc portd porte - port
		goodsab goodsce goodscd - goods
	)

	(:init
		(path porta portb)
		(path portb portc)
		(path portc portd)
		(path portd porte)
		(fuelat portc)
		(= (length porta portb) 5000)
		(= (length portb portc) 2500)
		(= (length portc portd) 3000)
		(= (length portd porte) 1500)
		(= (speed vessel0) 3)
		(goodsat goodsab portb)
		(vesselat vessel0 portc)
		(isdocked vessel0)
		(onboard goodscd vessel0)
		(onboard goodsce vessel0)
	)

	(:goal (and
		(vesselat vessel0 porte)
		(hasfueled vessel0)
		(goodsat goodsce porte)
		(goodsat goodscd portd)
	))

	(:metric minimize (total-time))
)
