import imu_sensor
import csv
import time

dt = 0.01
file_path = 'sensor_tests/log1.csv'
counter = 0
start_time = time.time()
time_elapsed = 0

IMU = imu_sensor.IMU()


while True:
	lin_acc_x = IMU.linear_acceleration[0]
	lin_acc_y = IMU.linear_acceleration[1]
	lin_acc_z = IMU.linear_acceleration[2]
	counter += 1
	with open(file_path, 'a', newline='') as file:
		writer = csv.writer(file)
		writer.writerow([lin_acc_x, lin_acc_y, lin_acc_z])
	print("Lin Acc: X: {}, Y: {}, Z: {}, Count: {}, Time: {}".format(lin_acc_x, lin_acc_y, lin_acc_z, counter, time_elapsed))
	time.sleep(dt)
	time_elapsed = time.time() - start_time


