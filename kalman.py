import numpy as np

def predict(x, P, A, Q, B=0, u=0): # x: state vector, P: covariance matrix, A: state transition matrix, Q: process variance
	x = np.dot(A, x) + np.dot(B, u)
	P = np.dot(A, np.dot(P, A.T)) + Q

	return x, P

def update(x, P, z, H, R): # H: observation matrix, z: measured values, R: measurement variance
	y = z - np.dot(H, x)
	S = R + np.dot(H, np.dot(P, H.T))
	K = np.dot(P, np.dot(H.T, np.linalg.pinv(S))) # Kalman Gain

	dim = z.shape[0]
	x = x + np.dot(K, y)
	P = np.dot((np.eye(dim) - np.dot(K, H)), np.dot(P, (np.eye(dim) - np.dot(K, H)))) + np.dot(K, np.dot(R, K.T))

	return x, P
