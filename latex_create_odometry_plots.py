import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

folder_name = "test_1/" # change this if new output.csv is desired (or just move test_1 to new name...
graph_path = "/home/pi/BEng_Project/sensor_tests/data/odometry/" + folder_name

dict = {"l_ticks": 0, "r_ticks": 1, "l_mm": 2, "r_mm": 3, "alpha": 4, "rad": 5, "x_old": 6, "vx_old": 7, "y_old": 8, "vy_old": 9, "theta_old": 10, "x": 11, "vx": 12, "y": 13, "vy":14, "theta": 15}

def load_data(file):
	data_lists = []
	for val in dict:
		data_lists.append([])
	with open(file, "r") as f:
		reader = csv.reader(f)
		for row in reader:
			for key, val in dict.items():
				data_lists[val].append(row[val])
	return data_lists

def lr_plot(data_lists):
	plt.figure() # adjust as necessary
	plt.subplot(111)
	plt.plot(data_lists[dict["l_mm"]], label="L (mm)")
	plt.plot(data_lists[dict["r_mm"]], label="R (mm)")
	plt.xlabel('Samples', fontsize=18)
	plt.ylabel('Motor distance (mm)', fontsize=16)
	plt.legend()
	plt.suptitle("L, R readings (mm)")
	plt.savefig(graph_path + "lr_plot.png")

def xy_plots(data_lists):
	plt.figure()
	plt.subplot(121)
	plt.plot(data_lists[dict["x"]], label="X (mm)")
	plt.plot(data_lists[dict["y"]], label="Y (mm)")
	plt.xlabel('Samples', fontsize=18)
	plt.ylabel('Position (mm)', fontsize=16)
	plt.legend()
	plt.subplot(122)
	plt.scatter(data_lists[dict["x"]], data_lists[dict["y"]])
	plt.xlabel('X Position (mm)', fontsize=18)
	plt.ylabel('Y Position (mm)', fontsize=16)
	plt.suptitle("X / Y Position")
	plt.savefig(graph_path + "xy_plots.png")

def theta_plot(data_lists):
	plt.figure()
	plt.subplot(111)
	plt.plot(data_lists[dict["theta"]], label="Theta (rad)")
	plt.xlabel("Samples", fontsize=18)
	plt.ylabel("Theta (rad)", fontsize=16)
	plt.legend()
	plt.suptitle("Theta (rad)")
	plt.savefig(graph_path + "theta_plot.png")

def main():
	data_lists = load_data(graph_path + "output.csv")
	lr_plot(data_lists)
	xy_plots(data_lists)
	theta_plot(data_lists)

if __name__ == "__main__":
	main()
