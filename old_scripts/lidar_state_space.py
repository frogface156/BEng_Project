import numpy as np

sig_position2 = Config['lidar']['sig_position2']

H = np.array([[1, 0, 0, 0, 0], [0, 0, 1, 0, 0]]) # potential for x', y' from previous state?
# Might want to look at the probabilities for different scan details - e.g. if not many features...
R = np.array([[sig_position2, 0], [0, sig_position2]]) # I'm assuming the probability is the same for both x and y

