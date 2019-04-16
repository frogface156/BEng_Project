Config = {
	'imu': {
		'sig_x2': 0.61**2, # standard deviation for x acceleration squared - do we have to use this? :'(
		'sig_y2': 0.01**2, # standard deviation for y accleration squared
		'sig_z2': 0.02**2, # standard deviation for z acceleration squared
		'sig_theta2': 0.1**2, # 22 / 1000 samples had a different value, the rest had the same value -> using a very low standard deviation, representing confidence in this reading. Not 0 sigmad because there were occasional weird readings, but pretty good!

		'x_bias': 0.87, # due to faulty sensor I think :'(
		'y_bias': 0, # very impressed with the y axis!
		'z_bias': -0.01, # also a good axis... use this instead of x axis!
		'theta_bias': 8, # adds 8 to all readings...

		'x_thresh': 2,
		'y_thresh': 4.5,
		'theta_thresh': 5
	},
	'odometry': {
		'sig_position2': 0.01**2, # DUMMY VALUE - populate with test value later...
		'sig_velocity2': 0.1**2, # DUMMY VALUE
		'sig_theta2': 0.1**2, # DUMMY VALUE - populate with test value later...
		'wheel_base': 250, # width of tank tracks - adjust to get a more accurate position tracking
		'ticks_to_mm': 1.082, # obtained with get_odometry_data.py and get_tick_factor.py
		'thresh': 18
	},
	'lidar': {
		'sig_position2': 0.1**2 # DUMMY VALUE - populate with test value later...
	},
	'robot': {
		'sig_trans2': 0.5**2 # DUMMY VALUE - populate with test value later...
	},
	'control': {
		'top_speed': 100, # max PWM code can output (actual maximum is 100)
		'motor_freq': 100, # PWM frequency (100 is good)
		'high_speed': 100, # PWM of the dominant motor for turning
		'low_speed': 10, # PWM of the submissive motor for turning
		'left_boost_factor': 1.5, # boost given to the left motor because it is weaker - would use PID controller but I don't have time :'(
		'pin_refs': {
			'in_1': 13,
			'in_2': 12,
			'in_3': 11,
			'in_4': 7,
			'en_a': 21,
			'en_b': 15,
		},
		'move_directions': {
			'forwards': {
				'in_1': False,
				'in_2': True,
				'in_3': True,
				'in_4': False
			},
			'backwards': {
				'in_1': True,
				'in_2': False,
				'in_3': False,
				'in_4': True
			},
			'stopped': {
				'in_1': False,
				'in_2': False,
				'in_3': False,
				'in_4': False
			}
		},
	},
	'pygame': {
		'fast_loop_freq': 80
	},
	'test': {
		'initial_state': {
			'x_0': 0,
			'vx_0': 0,
			'y_0': 0,
			'vy_0': 0,
			'theta_0': 0
		},
		'initial_probabilities': {
			'p0_x': 0,
			'p0_vx': 0,
			'p0_y': 0,
			'p0_vy': 0,
			'p0_theta': 0
		}
	},
	'logging': {
		'file_path': '/home/pi/BEng_Project/sensor_tests/',
		'extension': '.csv',
		'graph_file_path': '/home/pi/BEng_Project/sensor_tests/graphs/',
		'graph_extension': '.png'
	}
}
