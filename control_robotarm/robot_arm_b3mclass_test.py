import B3m_speed_servo

servo = B3m_speed_servo.B3M_class([0,0,0])
servo.start_arm()
servo.go_target_angle([0,0,90])
