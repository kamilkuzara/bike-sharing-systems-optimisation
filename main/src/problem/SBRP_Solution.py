from .Solution import Solution
import random

class SBRP_Solution(Solution):
    @staticmethod
    def compute_cost(vehicle_paths, distance_matrix):
        cost = 0

        for path in vehicle_paths:
            cost += Solution.compute_path_cost(path, distance_matrix)

        return cost

    @staticmethod
    def construct_from_OnePDTSPs(solutions, groups, problem):
        # reconstruct the solutions
        reconstructed_paths = []
        total_cost = 0
        for solution, group in zip(solutions, groups):
            total_cost += solution.cost

            reconstructed = []
            for vertex in solution.vehicle_path:
                reconstructed.append(group[vertex])

            reconstructed_paths.append(reconstructed)

        if len(reconstructed_paths) < problem.vehicle_num:
            missing_vehicles_num = problem.vehicle_num - len(reconstructed_paths)
            missing_paths = [ [0] for v in range(0, missing_vehicles_num) ]
            reconstructed_paths += missing_paths

        return SBRP_Solution(problem, reconstructed_paths, total_cost)

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
        tested_neighbours = set()

        stations_num = len(self._problem.requests)
        neighbourhood_size = stations_num * (self._problem.vehicle_num - 1)

        while len(tested_neighbours) < neighbourhood_size:
            # get the list of vehicles that visit some stations, i.e. their list does not just include the vertex 0
            non_empty_vehicles = [ vehicle for vehicle, path in enumerate(self._vehicle_paths) if len(path) > 1 ]

            # find a random valid vehicle from which a sub-path will be removed
            # old_vehicle = random.randint(0, self._problem.vehicle_num - 1)
            old_vehicle = random.choice(non_empty_vehicles)

            # get a random point on the old vehicle path from which it will be reassigned to a new vehicle
            reassignment_point = random.randint(1, len(self._vehicle_paths[old_vehicle]) - 1)

            # choose the new vehicle at random, it is different than the old vehicle
            new_vehicle = ( old_vehicle + random.randint(1, self._problem.vehicle_num - 1) ) % self._problem.vehicle_num

            neighbour_signature = str( (old_vehicle, reassignment_point, new_vehicle) )
            if neighbour_signature not in tested_neighbours:
                tested_neighbours.add( neighbour_signature )

                # the list of vehicle paths needs to be copied so that we do not ruin the original one
                new_paths = [ path.copy() for path in self._vehicle_paths ]

                station_1 = new_paths[old_vehicle][reassignment_point - 1] # new end of the old vehicle path
                station_2 = new_paths[old_vehicle][reassignment_point] # start of the path to reassign
                station_3 = new_paths[new_vehicle][-1] # current end of the new vehicle path, i.e. the point to which the path to reassign is appended

                # get the sub-path that is to be reassigned from one vehicle to another
                path_to_reassign = new_paths[old_vehicle][reassignment_point : ]

                # reassign the sub-path
                new_paths[new_vehicle] += path_to_reassign
                new_paths[old_vehicle] = new_paths[old_vehicle][0 : reassignment_point]

                if Solution.is_path_valid(new_paths[new_vehicle], self._problem.requests, self._problem.vehicle_capacity):   # the old vehicle path remains valid as we only remove stations from the end
                    new_cost = self.cost

                    # subtract the cost of edges that were removed
                    new_cost -= self._problem.distance_matrix[ station_1 ][ station_2 ]
                    new_cost -= self._problem.distance_matrix[ station_3 ][ 0 ]

                    # add the cost of edges that were added
                    new_cost += self._problem.distance_matrix[ station_1 ][ 0 ]
                    new_cost += self._problem.distance_matrix[ station_3 ][ station_2 ]

                    return SBRP_Solution(self._problem, new_paths, new_cost)

        return None

    def get_max_cost_difference(self):
        if len(self._problem.distance_matrix) == 1:
            return 0

        # flatten the distance matrix into a list of distances
        distances = [ dist for row in self._problem.distance_matrix for dist in row ]

        # sort the list in ascending order
        distances = sorted(distances)

        # compute the cost difference by subtracting the two shortest distances from the two longest
        return distances[len(distances) - 1] + distances[len(distances) - 2] - distances[0] - distances[1]
