import sensors
import csv
import time

save_name = input("Name of save file: ")
file_path = "/home/pi/BEng_Project/sensor_tests/{}.csv".format(save_name)


freq = 50
dt = 1 / freq

counter = 0
time_elapsed = 0

imu = sensors.IMU()

time.sleep(20)

start_time = time.time()

while True:
	lin_acc_x = imu.linear_acceleration[0]
	lin_acc_y = imu.linear_acceleration[1]
	lin_acc_z = imu.linear_acceleration[2]
	theta = imu.euler[0]
	counter += 1
	with open(file_path, 'a', newline='') as file:
		writer = csv.writer(file)
		writer.writerow([lin_acc_x, lin_acc_y, lin_acc_z, theta])
	print("Lin Acc: X: {}, Y: {}, Z: {}, Theta: {}, Count: {}, Time: {}".format(lin_acc_x, lin_acc_y, lin_acc_z, theta, counter, time_elapsed))
	time.sleep(dt)
	time_elapsed = time.time() - start_time


