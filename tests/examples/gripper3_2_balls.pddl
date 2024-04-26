(define (problem gripper3_2_balls)
	(:domain gripper3)

	(:objects
		rooma roomb - room
		ball1 ball2 - ball)

	(:init
		(free left)
		(free right)
		(at-robby rooma)
		(at-ball ball1 rooma)
		(at-ball ball2 rooma)
		(whole ball1)
		(whole ball2)
	)

	(:goal
		(and
			(at-ball ball1 roomb)
			(at-ball ball2 roomb)
			(whole ball1)
			(whole ball2)
			(at-robby roomb)
		)
	)
)
