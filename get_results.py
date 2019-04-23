import csv
import numpy as np

import kalman
import models
from Config import Config


path = "/home/pi/BEng_Project/sensor_tests/data/raw_sensor_data/straight/"
read_file = path + "raw_data_imu_odo_{}.csv"
final_vals_file = path + "final_values.csv"

odo_res = path + "odo_results.csv"
imu_res = path + "imu_results.csv"
odo_supp_res = path + "odo_supp_results.csv"
kal_res = path + "kalman_results.csv"

def log_data(file, data):
	with open(file, 'a') as f:
		writer = csv.writer(f)
		writer.writerow(data)

def clear_file(file):
	with open(file, 'w') as f:
		writer = csv.writer(f)

clear_file(odo_res)
clear_file(imu_res)
clear_file(odo_supp_res)
clear_file(kal_res)


def init():
	init = Config['test']['initial_state']
	x = np.array([[init['x_0'], init['vx_0'], init['y_0'], init['vy_0'], init['theta_0']]]).T
	P = np.array([[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]])
	oss = models.OdometryStateSpace()
	iss = models.IMUStateSpace()
	rss = models.RobotStateSpace()

	return x, P, oss, iss, rss

def get_odometry_results(file, vals, res_file, test_num, oss, x):
	ticks = []
	num_samples = 0
	file = file.format(test_num)
	with open(file, 'r') as f:
		reader = csv.reader(f)
		for row in reader:
			ticks.append((int(row[0]), int(row[1])))
			num_samples += 1

	real_x, real_y, real_theta = get_real_vals(vals, test_num)

	for l, r in ticks:
		l, r = oss.clean_input(l, r)
		x = oss.measure_state(x, l, r)

	data = [x[0][0], x[2][0], x[4][0], real_x, real_y, real_theta, num_samples]
	log_data(res_file, data)


def get_imu_results(file, vals, res_file, test_num, iss, x):
	imu_input = []
	num_samples = 0
	with open(file, 'r') as f:
		reader = csv.reader(f)
		for row in reader:
			imu_input.append((float(row[2]), float(row[3]), float(row[4])))
			num_samples += 1

	real_x, real_y, real_theta = get_real_vals(vals, test_num)

	for a_xi, a_yi, theta_i in imu_input:
		a_xi, a_yi, theta_i = iss.clean_input(a_xi, a_yi, theta_i)
		x = iss.measure_state(x, a_xi, a_yi, theta_i)
	data = [x[0][0], x[2][0], x[4][0], real_x, real_y, real_theta, num_samples]
	log_data(res_file, data)

def get_odometry_supp_results(file, vals, res_file, test_num, oss, iss, x):
	odo_supp_input = []
	num_samples = 0
	with open(file, 'r') as f:
		reader = csv.reader(f)
		for row in reader:
			odo_supp_input.append((int(row[0]), int(row[1]), float(row[4])))
			num_samples += 1

	a_xi = 0
	a_yi = 0

	real_x, real_y, real_theta = get_real_vals(vals, test_num)

	for l, r, theta_i in odo_supp_input:
		l, r = oss.clean_input(l, r)
		theta_i = (-1 * np.radians(theta_i - iss.theta_bias)) % (2*np.pi)
		x = oss.measure_state(x, l, r)
		x[4][0] = theta_i
	data = [x[0][0], x[2][0], x[4][0], real_x, real_y, real_theta, num_samples]
	log_data(res_file, data)

def get_kalman_results(file, vals, res_file, test_num, oss, iss, rss, x, P):
	raw_input = []
	num_samples = 0
	with open(file, 'r') as f:
		reader = csv.reader(f)
		for row in reader:
			raw_input.append((int(row[0]), int(row[1]), float(row[2]), float(row[3]), float(row[4])))
			num_samples += 1

	imu_a_x = 0
	imu_a_y = 0
	for l, r, ax, ay, ti in raw_input:
		z_i = iss.measure_state(x, imu_a_x, imu_a_y, ti)
		imu_a_x = ax
		imu_a_y = ay
		l, r = oss.clean_input(l, r)
		z_o = oss.measure_state(x, l, r)
		x, P = kalman.predict(x, P, rss.A, rss.Q)
		x, P = kalman.update(x, P, z_i, iss.H, iss.R)
		x, P = kalman.update(x, P, z_o, oss.H, oss.R)

	real_x, real_y, real_theta = get_real_vals(vals, test_num)

	data = [x[0][0], x[2][0], x[4][0], real_x, real_y, real_theta, num_samples]
	log_data(res_file, data)


def get_real_vals(vals, test_num):
	final_vals = []
	with open(vals, 'r') as f:
		reader = csv.reader(f)
		for row in reader:
			final_vals.append((int(row[0]), int(row[1]), int(row[2])))
	rx = final_vals[test_num][0]
	ry = final_vals[test_num][1]
	rtheta =  final_vals[test_num][2]

	return rx, ry, rtheta


for i in range(10):
	read_file = path + "raw_data_imu_odo_{}.csv".format(i+1)
	x, P, oss, iss, rss = init()
	get_odometry_results(read_file, final_vals_file, odo_res, i-1, oss, x)
	x, P, oss, iss, rss = init()
	get_imu_results(read_file, final_vals_file, imu_res, i-1, iss, x)
	x, P, oss, iss, rss = init()
	get_odometry_supp_results(read_file, final_vals_file, odo_supp_res, i-1, oss, iss, x)
	x, P, oss, iss, rss = init()
	get_kalman_results(read_file, final_vals_file, kal_res, i-1, oss, iss, rss, x, P)
