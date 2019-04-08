import pandas as pd
import csv
import numpy as np


file_path = "/home/pi/BEng_Project/sensor_tests/data/imu/"
file_name = "40_minutes_imu.csv"
file = file_path + file_name

x_vals = []
y_vals = []
z_vals = []
theta_a_vals = []
theta_b_vals = []
theta_c_vals = []
time_vals = []
dt = 1 / 60
counter = 0

with open(file, "r") as f:
	reader = csv.reader(f)
	for row in reader:
		x_vals.append(float(row[0]))
		y_vals.append(float(row[1]))
		z_vals.append(float(row[2]))
		theta_a_vals.append(float(row[3]))
		theta_b_vals.append(float(row[4]))
		theta_c_vals.append(float(row[5]))
		time_vals.append(dt * counter)
		counter += 1

x_sample = pd.Series(x_vals)
y_sample = pd.Series(y_vals)
z_sample = pd.Series(z_vals)
theta_a_sample = pd.Series(theta_a_vals)
theta_b_sample = pd.Series(theta_b_vals)
theta_c_sample = pd.Series(theta_c_vals)

def get_info(sample):
	mean = sample.mean()
	median = sample.median()
	sd_est = sample.std()
	sd_meas = sample.std(ddof=0)
	var = sample.var
	return [mean, median, sd_est, sd_meas, var]

x_info = get_info(x_sample)
y_info = get_info(y_sample)
z_info = get_info(z_sample)
theta_a_info = get_info(theta_a_sample)
theta_b_info = get_info(theta_b_sample)
theta_c_info = get_info(theta_c_sample)

print("Variable - Mean - Median - SD_Est - SD_Meas")
print("X-Axis - ", x_info[:4])
print("Y-Axis - ", y_info[:4])
print("Z-Axis - ", z_info[:4])
print("Theta_a - ", theta_a_info[:4])
print("Theta_b - ", theta_b_info[:4])
print("Theta_c - ", theta_c_info[:4])
