import sensors
import csv
import time

save_name = input("Name of save file: ")
file_path = "/home/pi/BEng_Project/sensor_tests/data/imu/{}.csv".format(save_name)


freq = 60
dt = 1 / freq

counter = 0
time_elapsed = 0

imu = sensors.IMU()

time.sleep(20) # to make sure I don't disturb the data!

start_time = time.time()

while True:
	lin_acc_x = imu.linear_acceleration[0]
	lin_acc_y = imu.linear_acceleration[1]
	lin_acc_z = imu.linear_acceleration[2]
	theta_a = imu.euler[0]
	theta_b = imu.euler[1]
	theta_c = imu.euler[2]
	counter += 1
	with open(file_path, 'a', newline='') as file:
		writer = csv.writer(file)
		writer.writerow([lin_acc_x, lin_acc_y, lin_acc_z, theta_a, theta_b, theta_c])
	print("Lin Acc: X: {}, Y: {}, Z: {}, Theta_a: {}, Theta_b: {}, Theta_c: {}, Count: {}, Time: {}".format(lin_acc_x, lin_acc_y, lin_acc_z, theta_a, theta_b, theta_c, counter, time_elapsed))
	time.sleep(dt)
	time_elapsed = time.time() - start_time


