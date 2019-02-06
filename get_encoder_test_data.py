import encoders
import time
import sys
import csv

no_list = ["no", "No", "n", "N", "q", "Q", "quit", "Quit"]
yes_list = ['', "y", "Y", "yes", "Yes"]
path = "sensor_tests/encoders/"
file_name = "encoder_data"
extension = ".csv"

log_file_path = path + file_name + extension

enc = encoders.encoder_handler()

ticks, ticks_last, ticks_dt = [0, 0], [0, 0], [0, 0]

def log_data(data):
	with open(log_file_path, "a") as f:
		writer = csv.writer(f)
		writer.writerow(data)

def start_test():
	input("Enter any key to start: ")
	while True:
		try:
			enc.update_ticks()
			enc.display_tick_count()
			time.sleep(0.05)
		except KeyboardInterrupt:
			final_ticks = enc.return_motor_info()
			break
	actual_distance = input("Enter actual distance travelled (mm): ")
	data = [final_ticks[0], final_ticks[1], actual_distance]
	print(data)
	log_data(data)
	quit_test()

def quit_test():
	response = input("Start another test? - y/n:")
	if response in no_list:
		sys.exit(1)
	elif response in yes_list:
		main()
	else:
		print("Invalid response. Try again.")
		quit_test()

def main():
	start_test()

if __name__ == "__main__":
	main()
