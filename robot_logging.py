import csv

def log_motor_ticks(log_file_path, time_at_reading, motor_ticks):
	with open(log_file_path, 'a') as log_file:
		writer = csv.writer(log_file)
		writer.writerow(['M', time_at_reading, motor_ticks[0], motor_ticks[1]])
