from .Problem import Problem
from .OnePDTSP_Solution import OnePDTSP_Solution
from .utils import depth_first_search

class OnePDTSP(Problem):
    # implements the generate_solution() method from the class Problem
    def generate_solution(self):
        vehicle_path = depth_first_search([0], self.distance_matrix, self.requests, 0, self.vehicle_capacity, self.vehicle_capacity)
        if vehicle_path is None:
            return None

        cost = OnePDTSP_Solution.compute_cost(vehicle_path, self.distance_matrix)

        return OnePDTSP_Solution(self, vehicle_path, cost)
