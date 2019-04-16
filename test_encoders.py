import sensors

l_ticks, r_ticks = 0, 0

enc = sensors.Encoders()
enc.get_ticks()

while True:
	l, r = enc.get_ticks()
	if ((l==0) or (r==0) or (l==None) or (r==None)):
		continue
	else:
		l_ticks += l
		r_ticks += r
		print("L: {}, R: {}".format(l_ticks, r_ticks))
