(define (domain triangle-tire)
  (:requirements :typing :strips :non-deterministic)
  (:types location)
  (:predicates (vehicle-at ?loc - location)
	       (spare-in ?loc - location)
	       (road ?from - location ?to - location)
	       (not-flattire))
  (:action move-car
    :parameters (?from - location ?to - location)
    :precondition (and (vehicle-at ?from) (road ?from ?to) (not-flattire))
    :effect (and (vehicle-at ?to) (not (vehicle-at ?from))
		 (oneof (and) (not (not-flattire)))))
  (:action changetire
    :parameters (?loc - location)
    :precondition (and (spare-in ?loc) (vehicle-at ?loc))
    :effect (and (not (spare-in ?loc)) (not-flattire)))
  (:action stay
    :parameters (?loc - location)
    :precondition (and (vehicle-at ?loc))
    :effect ())
  (:action test-car
    :parameters (?from - location)
    :precondition (and (vehicle-at ?from) (not-flattire))
    :effect (oneof (and) (not (not-flattire)))))