import imu_sensor

print("Initializing sensors...")

IMU = imu_sensor.IMU()

print("Initialization complete!\n")

while True:
	print("Linear Acceleration: {}".format(IMU.linear_acceleration))
