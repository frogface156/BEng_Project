import kalman
import numpy as np
import sensors
import models
from Config import Config
from pygame.time import Clock
import csv

test_num = input("Test Number: ")

graph_path = Config['logging']['graph_file_path']
extension = Config['logging']['graph_extension']
data_path = "/home/pi/BEng_Project/sensor_tests/data/raw_sensor_data/"
data_file_name = "raw_data_imu_odo_{}.csv".format(test_num)
data_file = data_path + data_file_name

final_vals_name = "final_values.csv"
final_vals_file = data_path + final_vals_name

with open(data_file, 'w') as f:
	writer = csv.writer(f)

freq = Config['pygame']['fast_loop_freq']
dt = 1 / freq

init_s = Config['test']['initial_state']
init_p = Config['test']['initial_probabilities']
x = np.array([[init_s['x_0'], init_s['vx_0'], init_s['y_0'], init_s['vy_0'], init_s['theta_0']]]).T
P = np.array([[init_p['p0_x'], 0, 0, 0, 0], [0, init_p['p0_vx'], 0, 0, 0], [0, 0, init_p['p0_y'], 0, 0], [0, 0, 0, init_p['p0_vy'], 0], [0, 0, 0, 0, init_p['p0_theta']]])

# Sensors
enc = sensors.Encoders()
imu = sensors.IMU()

N = 5000

imu_a_x = 0
imu_a_y = 0

def log_data(file, data):
	with open(file, "a") as f:
		writer = csv.writer(f)
		writer.writerow(data)

clock = Clock()
print("Starting...")
try:
	for i in range(N):
		data = []
		enc_l, enc_r = enc.get_ticks()
	#	if ((enc_l==None) or (enc_r==None)):
	#		pass
	#	else:
		data.append(enc_l)
		data.append(enc_r)
		imu_theta = imu.euler[0]
		data.append(imu_a_x)
		data.append(imu_a_y)
		data.append(imu_theta)
		imu_a_x = imu.linear_acceleration[2] # using the z-axis because x-axis is faulty...
		imu_a_y = imu.linear_acceleration[1]

		log_data(data_file, data)

		clock.tick(freq)

except KeyboardInterrupt:

	final_x = int(input("Final x value: "))
	final_y = int(input("Final y value: "))
	final_theta = int(input("Final theta value: "))

	final_data = [final_x, final_y, final_theta]

	log_data(final_vals_file, final_data)
