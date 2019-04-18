import csv
import numpy as np
from heapq import heappush, heappop

from Config import Config

s2 = np.sqrt(2)

class KinematicAStar(object):
	def __init__(self):
		self.path = []

	def plan_path(self, start, goal, obstacles):

		return path


class Dijkstra(object):
	def __init__(self):
		self.world_extents = Config['path_planning']['world_extents']
		self.world_obstacles = np.zeros(self.world_extents, dtype=np.uint8)
		self.movements = [
				(1, 0, 1.), (0, 1, 1.), (-1, 0, 1.), (0, -1, 1.),
				# comment this next line out to increase speed
				#(1, 1, s2), (-1, 1, s2), (1, -1, s2), (-1, -1, s2),
				]

	def plan_path(self, start, goal, obstacles):
		front = [ (0.001, start, None)]
		extents = obstacles.shape
		visited = np.zeros(extents, dtype=np.float32)
		came_from = {}
		while front:
			n = heappop(front)
			cost, pos, prev = n
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
							new_cost = cost + dcost
							print(new_cost, new_pos)
							heappush(front, (new_cost, new_pos, pos))
					else:
						continue

		path = []
		if pos == goal:
			while pos:
				path.append(pos)
				pos = came_from[pos]
			path.reverse()

		return (path, visited)

class AStar(object):
	def __init__(self):
		self.path = []

	def plan_path(self, start, goal):

		return path
