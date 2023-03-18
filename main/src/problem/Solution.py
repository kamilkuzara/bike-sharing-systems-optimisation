from abc import ABC, abstractmethod

class Solution(ABC):
    @staticmethod
    @abstractmethod
    def compute_cost(vehicle_paths, distance_matrix):
        return

    @staticmethod
    def compute_path_cost(path, distance_matrix):
        cost = 0
        for i in range(0, len(path) - 1):
            v = path[i]
            w = path[i+1]
            cost += distance_matrix[v][w]

        last_vertex = path[len(path) - 1]
        cost += distance_matrix[last_vertex][0]

        return cost

    def __init__(self, problem, cost):
        self._problem = problem
        self._cost = cost

    @property
    def cost(self):
        return self._cost

    @cost.setter
    def cost(self, new_cost):
        self._cost = new_cost

    @abstractmethod
    def is_valid(self):
        return

    @abstractmethod
    def generate_neighbour(self):
        return

    # The function returns the maximum absolute difference between the current solution (this object)
    # and its neighbours. It has to be implemented by each subclass because it's
    # result depends on the neighbourhood function
    @abstractmethod
    def get_max_cost_difference(self):
        return
