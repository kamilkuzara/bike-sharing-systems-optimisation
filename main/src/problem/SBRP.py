from .Problem import Problem
from .SBRP_Solution import SBRP_Solution
from .utils import depth_first_search, tabu_search

class SBRP(Problem):

    # implements the generate_solution() method from the class Problem
    def generate_solution(self):
        # assign each station to one of vehicle_num possible groups
        station_assignments = tabu_search(self.requests, self.vehicle_num, self.vehicle_capacity)
        # print(station_groups)     # <- for debugging only

        if station_assignments is None:
            return None

        # construct the actual vertex groups
        # NOTE: vertices in each group are sorted by ID in an increasing order
        #       which is important later on
        groups = [ [0] for vehicle in range(0, self.vehicle_num) ]
        for station, group in enumerate(station_assignments):
            groups[group].append(station + 1)

        # compute a vehicle path on each "non-empty" group, i.e. those that also
        # contain stations and not just the depot (a.k.a. vertex 0)
        vehicle_paths = []
        for group in groups:
            if len(group) == 1:
                vehicle_paths.append([0])
            else:
                # compute the distance matrix for the group of vertices
                group_distance_matrix = [ [dist for w, dist in enumerate(distances) if w in group] for v, distances in enumerate(self.distance_matrix) if v in group ]

                # compute the list of requests for the stations included in the group
                group_requests = [ request for station, request in enumerate(self.requests) if (station + 1) in group ]

                # find a valid path through the group
                path = depth_first_search([0], group_distance_matrix, group_requests, 0, self.vehicle_capacity, self.vehicle_capacity)

                # map the vertex indices from group back to general
                # NOTE: this is where it is important that the group is sorted
                # depot (vertex 0) will be mapped back to itself correctly
                for path_index, group_index in enumerate(path):
                    index = group[group_index]
                    path[path_index] = index

                vehicle_paths.append(path)

        # print(vehicle_paths)    # <- for debugging only

        cost = SBRP_Solution.compute_cost(vehicle_paths, self.distance_matrix)
        # print(cost) # <- for debugging only

        return SBRP_Solution(self, vehicle_paths, cost)
