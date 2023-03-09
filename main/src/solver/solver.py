import time
from .requests import compute_requests

def solve(coordinates, utilisation_data, vehicle_num, vehicle_capacity, algorithm = "simulated_annealing_on_SBRP"):
    # compute the requests for all stations
    start_time = time.time()
    requests = compute_requests(utilisation_data, vehicle_capacity)
    end_time = time.time()
    requests_computation_time = end_time - start_time

    # print(requests)   # <- for debugging only

    # check if the problem is solvable
    if abs(sum(requests)) > (vehicle_num * vehicle_capacity):
        print("The problem cannot be solved. Increase the number of vehicles or their capacity")
        return None # TODO: need to rethink if None should be returned here

    # TODO:
    # - choose the appropriate algorithm
