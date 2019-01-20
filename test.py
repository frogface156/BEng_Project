import imu_sensor

IMU = imu_sensor.IMU()
while True:
	print("Linear Acceleration: {}".format(IMU.linear_acceleration[0]))
