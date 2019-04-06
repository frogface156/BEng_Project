import kalman
import numpy as np
import random
from Config import Config
import sensors
import models
from pygame.time import Clock
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


graph_path = Config['logging']['graph_file_path']
extension = Config['logging']['graph_extension']

freq = Config['pygame']['fast_loop_freq']
dt = 1 / freq

init_s = Config['test']['initial_state']
init_p = Config['test']['initial_probabilities']
x = np.array([[init_s['x_0'], init_s['vx_0'], init_s['y_0'], init_s['vy_0'], init_s['theta_0']]]).T
P = np.array([[init_p['p0_x'], 0, 0, 0, 0], [0, init_p['p0_vx'], 0, 0, 0], [0, 0, init_p['p0_y'], 0, 0], [0, 0, 0, init_p['p0_vy'], 0], [0, 0, 0, 0, init_p['p0_theta']]])

rss = models.RobotStateSpace()
oss = models.OdometryStateSpace()

enc = sensors.Encoders()

x_predictions, x_corrections, x_measurements = [], [], []
y_predictions, y_corrections, y_measurements = [], [], []

N = 200

clock = Clock()
print("Starting...")
for i in range(N):
	enc_l, enc_r = enc.get_ticks()
	z_o = oss.measure_state(x, enc_l, enc_r)
	x_measurements.append(z_o[0][0])
	y_measurements.append(z_o[2][0])
	x, P = kalman.predict(x, P, rss.A, rss.Q)
	x_predictions.append(x[0][0])
	y_predictions.append(x[2][0])
	x, P = kalman.update(x, P, z_o, oss.H, oss.R)
	x_corrections.append(x[0][0])
	y_corrections.append(x[2][0])

	clock.tick(freq)

plt.plot(x_predictions, label='State Prediction')
plt.plot(x_measurements, label='Odometry Measurement')
plt.plot(x_corrections, label='Odometry Correction')
plt.legend()
plt.title("Kalman Filter - Odometry Test")

save_name = "KF_Odo_test"
plt.savefig(graph_path + save_name + extension)
