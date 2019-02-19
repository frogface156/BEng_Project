import imu_sensor
import i2c_class
import encoders
import encoder_matrix_test as emt
import numpy as np
import time
import datetime
import robot_logging as rl

# define variables
x_0 = 0
y_0 = 0
theta = 0
X = np.array([x_0, y_0])

freq = 0.5
dt_thresh = 1/freq

motor_ticks = [0, 0]

date = datetime.datetime.now().strftime("%H-%M-%S-%B-%d-%Y")
path = "sensor_tests/"
motor_file = "motor_ticks_"
camera_file = "camera_coords_"
imu_file = "imu_"
extension = ".csv"
file_num = 1
counter = 1

def get_file_path(sensor_file):
	log_file_path = path + sensor_file + date + extension
	return log_file_path

enc = encoders.encoder_handler()
IMU = imu_sensor.IMU()

start = time.time()
end = time.time()
dt_time = end - start

while True:

	'''
	if dt_time >= dt_thresh:
		enc.ticks_last = enc.ticks
		start = time.time()
	enc.return_motor_info() # update ticks
	enc.dt_ticks[0] = enc.ticks[0] - enc.ticks_last[0]
	enc.dt_ticks[1] = enc.ticks[1] - enc.ticks_last[1]
	end = time.time()
	dt_time = end - start
	print("Ticks_Last: {}".format(enc.ticks_last))
	print("Ticks_dt: {}".format(enc.dt_ticks))
	'''

	# Gather sample data loop (no processing / jumping time-steps)
	ticks = enc.return_motor_info() # update ticks
	dt_time = time.time() - start
	print("Ticks: {}\tTime: {}".format(ticks, dt_time))
	rl.log_motor_ticks(get_file_path(motor_file), dt_time, ticks) # log ticks
	lin_acc = IMU.linear_acceleration
	heading, roll, pitch = IMU.euler
	dt_time = time.time() - start
	print("Lin_Acc: {}\tHeading: {}, Time: {}".format(lin_acc, heading, dt_time))
	rl.log_imu(get_file_path(imu_file), dt_time, lin_acc, heading) # log imu
	print()
