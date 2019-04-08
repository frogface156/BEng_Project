import sensors
import models

lidar = sensors.LidarScanner()
lss = models.LidarStateSpace()

coords = []

for i in range(1):
	scan = lidar.get_scan(30, 0.04)
	obstacles = lss.get_obstacles(scan)
	print(obstacles)
