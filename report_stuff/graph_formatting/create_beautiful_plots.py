import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from my_plot import set_size
import numpy as np
import csv

#plt.style.use("seaborn") # Default style is better I think...
width = 452.9679 # obtained from LaTeX text width in my dissertation

nice_fonts = {
	# Use LaTex to write all text
	"text.usetex": True,
	"font.family": "serif",
	# Use 11pt (10 is standard but due to file conversions, I use 11) font in plots, to match 11 pt font in document
	"axes.labelsize": 11,
	"font.size": 11,
	# Make the legend/label fonts a little smaller
	"legend.fontsize": 9,
	"xtick.labelsize": 9,
	"ytick.labelsize": 9,
}

matplotlib.rcParams.update(nice_fonts) # LaTeX fonts and sizes for graphs!


###################################################################

file_path = "/home/pi/BEng_Project/sensor_tests/data/imu/"
file_name = "10_minutes_imu.csv"

file = file_path + file_name

x_vals = []
y_vals = []
z_vals = []
time_vals = []
dt = 1 / 60
counter = 0

with open(file, "r") as f:
	reader = csv.reader(f)
	for row in reader:
		x_vals.append(float(row[0]))
		y_vals.append(float(row[1]))
		z_vals.append(float(row[2]))
		time_vals.append(dt * counter)
		counter += 1

# x = np.linspace(0, 2*np.pi, 100) # from example...

# Initialise figure instance
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=set_size(width, subplot=[1, 2]))

# Plot
ax1.plot(time_vals, x_vals)
ax2.hist(np.array(x_vals), bins=280, edgecolor='black')
#fig.suptitle(r'IMU Linear Acceleration Probability Densities')
ax2.set_xlim(-0.5, 1.75)
#ax2.set_xlim(-0.25, 0.25)
#ax3.set_xlim(-0.25, 0.25)
ax1.set_xlabel(r'Time $(s)$')
ax1.set_ylabel(r'Acceleration $({m^2}/s)$')
ax2.set_ylabel(r'Frequency')
ax2.set_xlabel(r'Acceleration $({m^2}/s)$')
#ax2.set_xlabel(r'Acceleration $({m^2}/s)$')
#ax3.set_xlabel(r'Acceleration $({m^2}/s)$')
#ax1.set_title(r'x-axis')
#ax2.set_title(r'y-axis')
#ax3.set_title(r'z-axis')
#ax1.set_xlabel(r'$\theta$') # from example...
# ax.set_ylabel(r'$\sin{(\theta)}$') # from example...
#ax.legend()
#fig.suptitle(r'IMU Linear Acceleration')


# Save as PDF (no rasterising) and remove excess whitespace
plt.savefig('/home/pi/BEng_Project/report_stuff/graph_formatting/imu_plots_x.pdf', format='pdf', bbox_inches='tight')

