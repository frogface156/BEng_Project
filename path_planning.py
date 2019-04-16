import csv

from Config import Config



class KinematicAStar(object):
	def __init__(self):
		self.path = []

	def plan_path(self, start, goal, obstacles):

		return path


class Dijkstra(object):
	def __init__(self, start, goal):
		self.path = []
		self.start = start
		self.goal = goal

	def plan_path(self):
		front = [Node(self.start, cost=0)]
		while len(front) != 0:
			n = self.get_min_cost_node(front)
			n.visited = True
			for m in n.get_neighbours():
				front.append(m)

		return front

	def get_min_cost_node(self, list):
		n = None
		for node in list:
			if n:
				if (node.cost <  n.cost) and (node.visited == False):
					n = node
			else:
				n = node


		return n

class AStar(object):
	def __init__(self):
		self.path = []

	def plan_path(self, start, goal):

		return path

class Node(object):
	def __init__(self, coords, cost=None):
		self.coords = coords
		self.cost = cost
		self.visited = False
		self.previous = None
		self.moves = [(1, 0, 1), (0, 1, 1), (-1, 0, 1), (0, -1, 1), (1, 1, 1.4), (-1, 1, 1.4), (1, -1, 1.4), (-1, -1, 1.4)]

	def get_cost(self):

		return cost

	def get_neighbours(self):
		neighbours = []
		for move in self.moves:
			coords = (self.coords[0] + move[0], self.coords[1] + move[1])
			cost = self.cost + move[2]
			neighbours.append(Node(coords, cost))

		return neighbours
