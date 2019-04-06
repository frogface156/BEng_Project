import numpy as np
import kalman
import random

dt = 0.1
C = np.array([[1, 0], [0, 1]])
x = np.zeros((2,1))
z = np.array([[x[0, 0] + random.uniform(0, 1)], [x[1, 0] + random.uniform(0, 1)]])

P = np.diag((0.01, 0.01))
A = np.array([[1.0, dt], [0.0, 1.0]])
Q = np.eye(x.shape[0])
R = np.eye(z.shape[0])

N = 100

predictions, corrections, measurements = [], [], []

for k in np.arange(0, N):
	x, P = kalman.predict(x, P, A, Q)
	predictions.append(x)
	x, P = kalman.correct(x, C, z, P, Q, R)
	corrections.append(x)
	measurements.append(z)
	z = np.array([[x[0, 0] + random.uniform(0, 1)], [x[1, 0] + random.uniform(0, 1)]]) # test measurement

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
