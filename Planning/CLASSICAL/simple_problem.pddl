(define (problem simple) (:domain simple)
    (:objects
        vessel0 - vessel
        portA portB - port
        cont0 - cont
    )

    (:init
        (vesselAt vessel0 portA)
        (contAt cont0 portA)
    )

    (:goal (and
        (contAt cont0 portB)
    ))
)
