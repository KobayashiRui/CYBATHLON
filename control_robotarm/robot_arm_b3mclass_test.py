import B3m_speed_servo_lib

servo = B3m_speed_servo_lib.B3M_class()
#servo.start_arm()
servo.go_target_angle([-160,50,0])
