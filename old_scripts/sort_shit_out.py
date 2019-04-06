import encoders
import robot_logging as rl
import time
import csv


ticks = [0, 0]
ticks_last = [0, 0]
ticks_dt = [0, 0]

enc = encoders.encoder_handler()

dt_start = time.time()
dt_end = time.time()
freq = 4
dt = 1/freq

filename = "tick_log.csv"
count = 1

def get_ticks_dt(ticks, ticks_last):
	ticks_dt[0] = ticks[0] - ticks_last[0]
	ticks_dt[1] = ticks[1] - ticks_last[1]
	return ticks_dt

def print_info():
	print("Ticks: {}\tLast_ticks: {}\tdt_ticks: {}".format(ticks, ticks_last, ticks_dt))

def log_ticks_etc(row):
	with open(filename, 'a') as f:
		writer = csv.writer(f)
		writer.writerow(row)

while True:
	ticks = enc.return_motor_info()
	if (dt_end - dt_start) >= dt:
		print("1st Time: Ticks_last: {}".format(ticks_last))
#		ticks_dt[0] = ticks[0] - ticks_last[0]
#		ticks_dt[1] = ticks[1] - ticks_last[1]
		print("Ticks: {}".format(ticks))
#		ticks_last = ticks
		print("2nd Time: Ticks_last: {}".format(ticks_last))
		dt_start = time.time()
	#ticks_dt = get_ticks_dt(ticks, ticks_last)
	dt_end = time.time()
	row = [ticks, ticks_last, str(dt_end)]
	log_ticks_etc(row)
