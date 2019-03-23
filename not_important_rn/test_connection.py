import tcp_handler as tcp

host = "192.168.0.40"
port = 5000
c = tcp.get_server(host, port)

while True:
	data = tcp.recv_data(c)
	if data:
		print("Data: {}".format(data))

c.close()
