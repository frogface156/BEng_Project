import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from random import randint

from my_plot import set_size
import kinematic_astar as kstar


width = 452.9679 # obtained from LaTeX text width in my dissertation

nice_fonts = {
	# Use LaTex to write all text
	"text.usetex": True,
	"font.family": "serif",
	# Use 11pt (10 is standard but due to file conversions, I use 11) font in plots, to $
	"axes.labelsize": 11,
	"font.size": 11,
	# Make the legend/label fonts a little smaller
	"legend.fontsize": 9,
	"xtick.labelsize": 9,
	"ytick.labelsize": 9,
}

matplotlib.rcParams.update(nice_fonts) # LaTeX fonts and sizes for graphs!

#obstacles = []
#for i in range(4):
#	ob = (randint(0, 50), randint(0, 50))
#	obstacles.append(ob)

#obstacles = [(0, 30), (5, 30), (10, 30), (15, 30), (20, 30), (50, 55), (50, 50), (50, 45), (50, 40), (50, 35), (50, 30), (50, 25), (50, 20), (50, 15), (50, 10), (30, 60), (35, 60), (40, 60)]
obstacles = [(3, 40), (9, 40), (15, 40), (21, 40), (62, 75), (54, 75), (48, 75), (42, 75), (65, 0), (65, 5), (65, 10), (65, 15), (65, 20), (65, 25), (65, 30), (65, 35), (65, 40), (65, 45), (65, 50), (65, 55), (65, 60), (65, 65)]

extents = (70, 100)
pp = kstar.KinematicAStar(extents)
#start = (randint(0, 10), randint(0, 10), np.radians(randint(0, 20)))
#goal = (randint(40, 50), randint(40, 50), np.radians(randint(30, 50)))
#path, moves, visited, obstacles_array = pp.plan_path(start, goal, obstacles)
path, moves, visited, obstacles_array = pp.plan_path((10, 0, np.radians(90)), (31, 90, np.radians(90)), obstacles)
print(path)
print(moves)

x_vals = []
y_vals = []

for node in path:
	x_vals.append(node[0])
	y_vals.append(node[1])

fig, ax1 = plt.subplots(1, 1, figsize=set_size(width, subplot=[1, 1]))
ax1.scatter(x_vals, y_vals, c='#ff7f0e')
ax1.set_xlabel(r'x-axis')
ax1.set_xlim(0, extents[0])
ax1.set_ylim(0, extents[1])
ax1.set_ylabel(r'y-axis')
ax1.matshow(obstacles_array.T, cmap='Blues')
plt.savefig('/home/pi/BEng_Project/report_stuff/graph_formatting/path_planning.pdf', format='pdf', bbox_inches='tight')
