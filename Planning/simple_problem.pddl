(define (problem simple) (:domain simple_graphplan)
    (:objects
        vessel0 - vessel
        portA portB portC portD - port
    )

    (:init
        (at vessel0 portA)
        (path portA portB) (path portB portC) (path portC portD)
    )

    (:goal (and
        (at vessel0 portD)
    ))
)