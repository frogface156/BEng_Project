import csv
import numpy as np
from heapq import heappush, heappop
import scipy.ndimage

from Config import Config

s2 = np.sqrt(2)


class AStar(object):
	def __init__(self):
		self.world_extents = Config['path_planning']['world_extents']
		self.world_obstacles = np.zeros(self.world_extents, dtype=np.uint8)
		self.obstacle_avoidance_factor = Config['path_planning']['obstacle_avoidance_factor']
		self.use_potential_function = True
		self.movements = [
				(1, 0, 1.), (0, 1, 1.), (-1, 0, 1.), (0, -1, 1.),
				# comment this next line out to increase speed
				#(1, 1, s2), (-1, 1, s2), (1, -1, s2), (-1, -1, s2),
				]

	def plan_path(self, start, goal, obstacles):
		self.clear_obstacles()
		for i in obstacles:
			self.add_obstacle(i)
		self.apply_distance_transform()
		front = [ (self.distance(start, goal), 0.001, start, None)]
		extents = self.world_obstacles.shape
		visited = np.zeros(extents, dtype=np.float32)
		came_from = {}
		while front:
			n = heappop(front)
			total_cost, cost, pos, prev = n
			if visited[pos] > 0:
				pass
			else:
				visited[pos] = cost
				came_from.update({pos : prev})
				if pos == goal:
					print("Reached Goal: {}".format(pos))
					break # goal reached!
				for dx, dy, dcost in self.movements:
					new_x = pos[0] + dx
					new_y = pos[1] + dy
					if (0 <= new_x < extents[0]) and (0 <= new_y < extents[1]):
						new_pos = (new_x, new_y)
						if (visited[new_pos] == 0) and (self.world_obstacles[new_pos] != 255):
							new_cost = cost + dcost + (self.world_obstacles[pos] / self.obstacle_avoidance_factor)
							new_total_cost = new_cost + self.distance(new_pos, goal) + (self.world_obstacles[pos] / self.obstacle_avoidance_factor)
							heappush(front, (new_total_cost, new_cost, new_pos, pos))
					else:
						continue

		path = []
		if pos == goal:
			while pos:
				path.append(pos)
				pos = came_from[pos]
			path.reverse()

		return (path, visited, self.world_obstacles)

	@staticmethod
	def distance(p, q): # euclidean distance between two points
		return np.sqrt((p[0] - q[0])**2 + (p[1] - q[1])**2)

	def set_obstacle(self, pos, on):
		N = 2  # Box size will be 2N+1
		x, y = pos
		l = max(0, x-N)
		r = min(self.world_extents[0]-1, x+N)
		d = max(0, y-N)
		u = min(self.world_extents[1]-1, y+N)
		if l<=r and d<=u:
			if on:
				mask = np.ones((r-l+1, u-d+1)) * 255
			else:
				mask = np.zeros((r-l+1, u-d+1))
			self.world_obstacles[l:r+1, d:u+1] = mask

	def add_obstacle(self, pos):
		self.set_obstacle(pos, True)

	def clear_obstacles(self):
		self.world_obstacles = np.zeros(self.world_extents, dtype=np.uint8)

	def apply_distance_transform(self):
		if self.use_potential_function and np.max(self.world_obstacles) == 255:
			# Compute distance transform.
			dist_transform = 255-np.minimum(
				16*scipy.ndimage.morphology.distance_transform_edt(
				255-self.world_obstacles), 255)
			m = max(np.max(dist_transform), 1)  # Prevent m==0.
			self.world_obstacles = np.uint8((dist_transform * 255) / m)
		else:
			# Keep 255 values only (set all other to 0).
			self.world_obstacles = (self.world_obstacles == 255) * np.uint8(255)
