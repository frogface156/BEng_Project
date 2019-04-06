import numpy as np

def predict(x, P, A, Q): # x: state vector, P: covariance matrix, A: state transition matrix, Q: process variance
	x = np.dot(A, x)
	P = np.dot(A, np.dot(P, A.T)) + Q

	return x, P

def correct(x, C, z, P, Q, R): # C: observation matrix, z: measured values, R: measurement variance
	S = np.dot(C, np.dot(P, C.T)) + R
	K = np.dot(P, np.dot(C.T, np.linalg.inv(S)))

	x = x + np.dot(K, (z - np.dot(C, x)))
	P = P - np.dot(K, np.dot(S, K.T))

	return x, P
