from abc import ABC, abstractmethod

class Problem(ABC):
    def __init__(self, distance_matrix, requests, vehicle_num, vehicle_capacity):
        self.distance_matrix = distance_matrix
        self.requests = requests
        self.vehicle_num = vehicle_num
        self.vehicle_capacity = vehicle_capacity

    # def find_vehicle_path(self, path, min_load, max_load):
    #     if len(path) == len(self.distance_matrix):
    #         return path
    #
    #     # find reachable vertices
    #     reachable = []
    #     for vertex, request in enumerate(self.requests):
    #         if vertex not in path and min_load + request
    #             reachable.append(vertex)
    #
    #     for vertex in reachable:
    #         request = self.requests[vertex]
    #         final_path = self.find_vehicle_path(path + [vertex], max(min_load + request, 0), min(max_load + request, self.vehicle_capacity))
    #         if final_path is not None:
    #             return final_path
    #
    #     return None

    # This needs to be an abstract method, to be implemented by each concrete class
    # It is a standard method (i.e. neither a class method nor a static method)
    @abstractmethod
    def generate_solution():
        return
