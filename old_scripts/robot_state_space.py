import numpy as np
from Config import Config

sig_trans2 = Config['robot']['sig_trans2'] # DUMMY VARIABLE - can't use for all in diagonal

freq = Config['pygame']['fast_loop_freq']
dt = 1 / freq

Q = sig_trans2*np.eye(5) # DUMMY MATRIX - will need to get values from testing
A = np.array([[1, dt, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 1, dt, 0], [0, 0, 0, 1, 0], [0, 0, 0, 0, 1]])
