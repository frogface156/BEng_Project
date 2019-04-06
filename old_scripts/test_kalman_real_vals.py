import numpy as np
import kalman
import random
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from Config import Config

dt = 0.1
C = np.array([[1, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0]]) # observe x, y
x = np.zeros((6, 1)) # start position, velocity, acceleration = 0
z = np.array([[x[0, 0] + random.uniform(0, 1)], [x[1, 0] + random.uniform(0, 1)]])

P = np.diag((0.01, 0, 0, 0.01, 0, 0))
A = np.array([[1.0, dt, 0.5*dt**2, 0, 0, 0], [0.0, 1.0, dt, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 1, dt, 0.5*dt**2], [0, 0, 0, 0, 1, dt], [0, 0, 0, 0, 0, 0]])
B = np.array([[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1]])
u = np.array([0, 0, random.uniform(0, 2), 0, 0, random.uniform(0, 2)])
#u = np.array([0, 0, 1, 0, 0, 1])
#Q = np.eye(x.shape[0])
sq2 = 0.1**2
Q = np.array([[0.5*(dt**2)*sq2, 0, 0, 0, 0, 0], [0, dt*sq2, 0, 0, 0, 0], [0, 0, sq2, 0, 0, 0], [0, 0, 0, 0.5*(dt**2)*sq2, 0, 0], [0, 0, 0, 0, dt*sq2, 0], [0, 0, 0, 0, 0, sq2]])
R = 0.01*np.eye(z.shape[0])

N = 100

predictions, corrections, measurements = [], [], []

for k in np.arange(0, N):
	x, P = kalman.predict(x, P, A, B, u, Q)
	predictions.append(x)
	x, P = kalman.correct(x, C, z, P, R)
	corrections.append(x)
	measurements.append(z)
	z = np.array([[x[0, 0] + random.uniform(0, 1)], [x[1, 0] + random.uniform(0, 1)]]) # test measurement

measurements_plot_x = []
predictions_plot_x = []
corrections_plot_x = []
measurements_plot_y = []
predictions_plot_y = []
corrections_plot_y = []

for x in range(10):
	print("TEST: Predictions: {}".format(predictions[x][0][0]))

for x in measurements:
	measurements_plot_x.append(x[0])
	measurements_plot_y.append(x[1])
for x in predictions:
	predictions_plot_x.append(x[0][0])
	predictions_plot_y.append(x[3])
for x in corrections:
	corrections_plot_x.append(x[0][0])
	corrections_plot_y.append(x[3])

plt.plot(measurements_plot_x, label='True Values - X')
plt.plot(predictions_plot_x, label='Predicted Values - X')
plt.plot(corrections_plot_x, label='Corrected Values - X')
#plt.plot(measurements_plot_y, label='True Values - Y')
#plt.plot(predictions_plot_y, label='Predicted Values - Y')
#plt.plot(corrections_plot_y, label='Corrected Values - Y')
plt.legend()
plt.title('Kalman Filter Test - using simluated IMU and Measurement Values')

plt.savefig("Kalman_Plot.png")

pred_final = predictions[-1][0]
meas_final = measurements[-1][0]
corr_final = corrections[-1][0]
pred_error = abs(pred_final - corr_final)
meas_error = abs(meas_final - corr_final)

print("Predicted final estimate: {}".format(pred_final))
print("Measured final state: {}".format(meas_final))
print("Corrected final estimate: {}".format(corr_final))
print()
print("Prediction error: {}".format(pred_error))
print("Measurement error: {}".format(meas_error))
