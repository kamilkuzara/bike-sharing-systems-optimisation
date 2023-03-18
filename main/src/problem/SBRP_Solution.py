from .Solution import Solution

class SBRP_Solution(Solution):
    @staticmethod
    def compute_cost(vehicle_paths, distance_matrix):
        cost = 0

        for path in vehicle_paths:
            cost += Solution.compute_path_cost(path, distance_matrix)

        return cost

    def __init__(self, problem, vehicle_paths, cost):
        self._vehicle_paths = vehicle_paths
        super().__init__(problem, cost)

    def is_valid(self):
        pass
        # for each path check if it's valid
        # for path in self._vehicle_paths:
        #   if not is_path_valid(path, self._problem.requests)
        #       return False
        # return True

    def generate_neighbour(self):
        pass

    def get_max_cost_difference(self):
        if len(self._problem.distance_matrix) == 1:
            return 0

        # flatten the distance matrix into a list of distances
        distances = [ dist for row in self._problem.distance_matrix for dist in row ]

        # sort the list in ascending order
        distances = sorted(distances)

        # compute the cost difference by subtracting the two shortest distances from the two longest
        return distances[len(distances) - 1] + distances[len(distances) - 2] - distances[0] - distances[1]
