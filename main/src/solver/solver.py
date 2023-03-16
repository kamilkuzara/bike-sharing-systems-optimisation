import time
from .requests import compute_requests
from .distance import compute_distance_matrix
from problem import SBRP
from algorithms import simulated_annealing


# def solve_OnePDTSP(coordinates, requests, vehicle_num, vehicle_capacity):
#     # compute the distance matrix
#     distance_matrix = compute_distance_matrix(coordinates)
#
#     # create an instance of the problem
#     problem = OnePDTSP(distance_matrix, requests, vehicle_num, vehicle_capacity)
#
#     start_time = time.time()
#     solution = simulated_annealing(problem)
#     end_time = time.time()
#     solution_time = end_time - start_time
#
#     return solution, solution_time
#
def solve_multiple_OnePDTSP(coordinates, requests, vehicle_num, vehicle_capacity):
    pass
#     # divide the stations into groups
#     groups = compute_station_groups(coordinates, requests)
#
#     # Note: a mapping of groups is needed so that the solutions can be combined in the final step
#
#     solutions = []
#     total_time = 0
#     for group in groups:
#         # solve a single OnePDTSP
#         solution, solution_time = solve_OnePDTSP()
#         solutions.append(solution)
#         total_time += solution_time
#
#     # combine the OnePDTSP solutions into a SBRP solution
#
#     return final_solution, total_time
#
#     # # TODO:
#     # # compute distance matrix for each group
#     # # create an instance of the OnePDTSP for each group of stations
#     #
#     # # solve each of the smaller OnePDTSP problems
#     # solutions = []
#     # for problem in problems:
#     #     solution = simulated_annealing(problem)
#     #     solutions.append(solution)
#     #

# function only for degugging
def print_m(matrix):
    for line in matrix:
        print(line)
    print()

def solve_SBRP(coordinates, requests, vehicle_num, vehicle_capacity):
    # compute the distance matrix
    distance_matrix = compute_distance_matrix(coordinates)
    # print_m(distance_matrix)  # <- for debugging only

    # create an instance of the problem
    problem = SBRP(distance_matrix, requests, vehicle_num, vehicle_capacity)

    solution = simulated_annealing(problem)

    return solution

algorithms = {
    "1": {
        "algorithm": solve_SBRP,
        "description": "Static Bike Repositioning Problem - Simulated Annealing algorithm"
    },
    "2": {
        "algorithm": solve_multiple_OnePDTSP,
        "description": "multiple instances of One-Commodity Pickup-Delivery TSP - Simulated Annealing algorithm"
    }
}

def solve(coordinates, utilisation_data, vehicle_num, vehicle_capacity, algorithm = "1"):
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

    # choose and run the appropriate solution approach
    start_time = time.time()
    solution = algorithms.get(algorithm).get("algorithm")(coordinates, requests, vehicle_num, vehicle_capacity)
    end_time = time.time()
    solution_time = end_time - start_time

    # TODO:
    # - return the results in an appropriate form
