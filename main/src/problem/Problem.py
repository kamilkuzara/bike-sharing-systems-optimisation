from abc import ABC, abstractmethod

class Problem(ABC):
    def __init__(self, distance_matrix, requests, vehicle_num, vehicle_capacity):
        self._distance_matrix = distance_matrix
        self._requests = requests
        self._vehicle_num = vehicle_num
        self._vehicle_capacity = vehicle_capacity

    @property
    def distance_matrix(self):
        return self._distance_matrix

    @property
    def requests(self):
        return self._requests

    @property
    def vehicle_num(self):
        return self._vehicle_num

    @property
    def vehicle_capacity(self):
        return self._vehicle_capacity

    # This needs to be an abstract method, to be implemented by each concrete class
    # It is a standard method (i.e. neither a class method nor a static method)
    @abstractmethod
    def generate_solution(self):
        return
