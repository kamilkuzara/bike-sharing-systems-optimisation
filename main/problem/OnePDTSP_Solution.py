from .Solution import Solution
import random

class OnePDTSP_Solution(Solution):
    @staticmethod
    def compute_cost(vehicle_path, distance_matrix):
        return Solution.compute_path_cost(vehicle_path, distance_matrix)

    def __init__(self, problem, vehicle_path, cost):
        self._vehicle_path = vehicle_path
        super().__init__(problem, cost)

    @property
    def vehicle_path(self):
        return self._vehicle_path

    def is_valid(self):
        pass

    def generate_neighbour(self):
        # the network only contains the depot (vertex 0) and one station
        if len(self._problem.distance_matrix) <= 2:
            return None

        tested_neighbours = set()

        num_vertices = len(self._problem.distance_matrix)
        neighbourhood_size = num_vertices * (num_vertices - 3)

        while len(tested_neighbours) < neighbourhood_size:
            v = random.randint(0, len(self._vehicle_path) - 1)
            w = (v + random.randint(2, len(self._vehicle_path) - 2)) % len(self._vehicle_path)

            point_1 = min(v, w)
            point_2 = max(v, w)

            neighbour_signature = str( (point_1, point_2) )
            if neighbour_signature not in tested_neighbours:
                tested_neighbours.add(neighbour_signature)

                new_path = []

                # construct the new path with the 2-opt change
                index = 0
                step = 1
                while index < len(self._vehicle_path):
                    vertex = self._vehicle_path[index]
                    new_path.append(vertex)

                    if index == point_1:
                        index = point_2
                        step = -1
                    elif index == point_1 + 1:
                        index = point_2 + 1
                        step = 1
                    else:
                        index += step

                # check if the new solution is valid
                if Solution.is_path_valid(new_path, self._problem.requests, self._problem.vehicle_capacity):
                    new_cost = OnePDTSP_Solution.compute_cost(new_path, self._problem.distance_matrix)

                    return OnePDTSP_Solution(self._problem, new_path, new_cost)

        return None
        # Alternative way of generating a neighbour - reverse some sequence of stations:
        # start = random.randint(1, len(self._vehicle_path) - 2)
        # end = random.randint(start + 2, len(self._vehicle_path))
        #
        # new_path = self._vehicle_path.copy()
        #
        # new_path[start:end] = new_path[start:end][::-1]


    def get_max_cost_difference(self):
        if len(self._problem.distance_matrix) == 1:
            return 0

        # flatten the distance matrix into a list of distances
        distances = [ dist for row in self._problem.distance_matrix for dist in row ]

        # sort the list in ascending order
        distances = sorted(distances)

        # compute the cost difference by subtracting the n-1 shortest distances from the n-1 longest,
        # where n is the number of vertices
        num_vertices = len(self._problem.distance_matrix)
        return sum(distances[len(distances) - num_vertices + 1 : ]) - sum(distances[ : num_vertices - 1])
