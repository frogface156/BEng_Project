import csv
import numpy as np
from heapq import heappush, heappop
import scipy.ndimage
from math import sqrt, sin, cos, pi, radians, copysign, floor

from Config import Config


class KinematicAStar(object):
	def __init__(self, extents=None):
		if extents:
			self.world_extents = extents
		else:
			self.world_extents = Config['path_planning']['world_extents']
		self.world_obstacles = np.zeros(self.world_extents, dtype=np.uint8)
		self.obstacle_avoidance_factor = Config['path_planning']['obstacle_avoidance_factor']
		self.use_potential_function = Config['path_planning']['potential_function']
		curv = Config['path_planning']['segment_curvature']
		length = Config['path_planning']['segment_length']
		bcost = Config['path_planning']['backwards_cost_multiplier']
		self.movements = [(curv, length), (0, length), (-curv, length)]
		self.backwards_movements =[(curv, -length), (0, -length), (-curv, -length)]
		if Config['path_planning']['backwards_motion']:
			self.movements.extend(self.backwards_movements)
		self.move_count = len(self.movements)

	def plan_path(self, start, goal, obstacles):
		self.clear_obstacles()
		for i in obstacles:
			self.add_obstacle(i)
		self.apply_distance_transform()
		front = [ (self.distance(start, goal), 0.001, start, None, None)] # total cost, cost, pose, prev_pose, move
		extents = self.world_obstacles.shape
		visited = np.zeros(extents, dtype=np.float32)
		generated_states = {}
		while front:
			if len(front) > 400000:
				print("Took ages... Gave up.")
				break
			total_cost, cost, pose, prev_pose, move = heappop(front)
			discrete_pose = self.pose_index(pose)
			if discrete_pose in generated_states:
				continue
			visited[int(pose[0]), int(pose[1])] = cost
			generated_states.update({discrete_pose : (prev_pose, move)})
			if self.states_close(pose, goal):
				print("Reached Goal: {}".format(pose))
				break
			for i in range(self.move_count):
				curv, length = self.movements[i]
				new_pose = CurveSegment.end_pose(pose, curv, length)
				if not (0 <= new_pose[0] < extents[0] and \
					0 <= new_pose[1] < extents[1]):
					continue
				if not self.world_obstacles[(int(new_pose[0]), int(new_pose[1]))] == 255:
					obstacle_cost = self.world_obstacles[(int(new_pose[0]), int(new_pose[1]))] / self.obstacle_avoidance_factor
					new_cost = cost + abs(length) + obstacle_cost
					total_cost = new_cost + self.distance(new_pose, goal)
					heappush(front, (total_cost, new_cost, new_pose, pose, i))
				else:
					continue
		if self.states_close(pose, goal):
			path = []
			moves = []
			path.append(pose[0:2])
			pose, move = generated_states[self.pose_index(pose)]
			while pose:
				moves.append(move)
				points = CurveSegment.segment_points(pose, self.movements[move][0], self.movements[move][1], 2.0)
				path.extend(reversed(points))
				pose, move = generated_states[self.pose_index(pose)]
			path.reverse()
			moves.reverse()
		else:
			path = []
			moves = []

		return (path, moves, visited, self.world_obstacles)

	@staticmethod
	def distance(p, q): # euclidean distance between two points
		return np.sqrt((p[0] - q[0])**2 + (p[1] - q[1])**2)

	def set_obstacle(self, pos, on):
		N = 1  # Box size will be 2N+1
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

	def states_close(self, p, q):
		d_angle = abs((p[2]-q[2]+pi) % (2*pi) - pi)
		# tolerance of 15 degrees for heading, 2.0 for the position.
		return d_angle < radians(15.0) and self.distance(p, q) <= 2.0

	@staticmethod
	def pose_index(pose):
		pos_raster = 1.0
		heading_raster = radians(10.)
		xi = int(floor(pose[0] / pos_raster))
		yi = int(floor(pose[1] / pos_raster))
		ti = int(floor(pose[2] / heading_raster))
		return (xi, yi, ti)

class CurveSegment:
	@staticmethod
	def end_pose(start_pose, curvature, length):
		x, y, theta = start_pose
		if curvature == 0.0:
			# Linear movement.
			x += length * cos(theta)
			y += length * sin(theta)
			return (x, y, theta)
		else:
			# Curve segment of radius 1/curvature.
			tx = cos(theta)
			ty = sin(theta)
			radius = 1.0/curvature
			xc = x - radius * ty  # Center of circle.
			yc = y + radius * tx
			angle = length / radius
			cosa = cos(angle)
			sina = sin(angle)
			nx = xc + radius * (cosa * ty + sina * tx)
			ny = yc + radius * (sina * ty - cosa * tx)
			ntheta = (theta + angle + pi) % (2*pi) - pi
			return (nx, ny, ntheta)

	@staticmethod
	def segment_points(start_pose, curvature, length, delta_length):
		"""Return points of segment, at delta_length intervals."""
		l = 0.0
		delta_length = copysign(delta_length, length)
		points = []
		while abs(l) < abs(length):
			points.append(CurveSegment.end_pose(start_pose, curvature, l)[0:2])
			l += delta_length
		return points
