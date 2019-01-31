import encoders
import time

enc = encoders.encoder_handler()

while True:
	try:
		start = time.time()
		enc.update_states()
		enc.update_ticks()
		end = time.time()
		#enc.print_states()
		enc.print_ticks()
		loop = end - start
		print("Loop took {}s".format(loop))

	except KeyboardInterrupt:
		enc.cleanup()
		break
