Config = {
	'imu': {
		'sig_x2': 0.61**2, # standard deviation for x acceleration squared - do we have to use this? :'(
		'sig_y2': 0.01**2, # standard deviation for y accleration squared
		'sig_z2': 0.02**2, # standard deviation for z acceleration squared
		'sig_theta2': 0.001**2, # 22 / 1000 samples had a different value, the rest had the same value -> using a very low standard deviation, representing confidence in this reading. Not 0 sigmad because there were occasional weird readings, but pretty good!
		'x_bias': 0.87, # due to faulty sensor I think :'(
		'y_bias': 0, # very impressed with the y axis!
		'z_bias': -0.01, # also a good axis... use this instead of x axis!
		'theta_bias': 8 # adds 8 to all readings...
	},
	'odometry': {
		'sig_position2': 0.1**2, # DUMMY VALUE - populate with test value later...
		'sig_theta2': 0.1**2, # DUMMY VALUE - populate with test value later...
		'wheel_base': 163, # width of tank tracks - adjust to get a more accurate position tracking
		'ticks_to_mm': 0.78 # obtained with get_odometry_data.py and get_tick_factor.py
	},
	'lidar': {
		'sig_position2': 0.1**2 # DUMMY VALUE - populate with test value later...
	},
	'robot': {
		'sig_trans2': 0.5**2 # DUMMY VALUE - populate with test value later...
	},
	'control': {

	},
	'pygame': {
		'fast_loop_freq': 50
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
			'p0_x': 0.1,
			'p0_vx': 0.1,
			'p0_y': 0.1,
			'p0_vy': 0.1,
			'p0_theta': 0.1
		}
	},
	'logging': {
		'file_path': '/home/pi/BEng_Project/sensor_tests/',
		'extension': '.csv',
		'graph_file_path': '/home/pi/BEng_Project/sensor_tests/graphs/',
		'graph_extension': '.png'
	}
}
