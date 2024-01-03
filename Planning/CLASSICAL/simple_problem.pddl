(define (problem simple) (:domain simple)
    (:objects
        vessel0 - vessel
        portA portB - port
        cont0 - cont
    )

    (:init
        (at vessel0 portA)
        (at cont0 portA)
    )

    (:goal (and
        (at cont0 portB)
    ))
)
