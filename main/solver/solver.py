import time
from .requests import compute_requests
from .distance import compute_distance_matrix
from .grouping import compute_station_groups
from problem import SBRP, OnePDTSP, SBRP_Solution
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
def solve_multiple_OnePDTSP(coordinates, requests, vehicle_num, vehicle_capacity, hyperparameters):
    # compute the distance matrix
    distance_matrix = compute_distance_matrix(coordinates)

    # compute the distance matrix only for stations
    stations_distance_matrix = [ row[1:] for row in distance_matrix[1:] ]

    # divide the stations into groups
    group_assignments, num_groups = compute_station_groups(coordinates[1:], stations_distance_matrix, requests, vehicle_num, vehicle_capacity)

    if group_assignments is None:
        return None

    # compute the groups
    groups = [ [0] for g in range(0, num_groups) ]
    for station, group in enumerate(group_assignments):
        vertex = station + 1
        groups[group].append(vertex)

    # solve OnePDTSP on each group
    solutions = []
    for group in groups:
        # compute the distance matrix for the group of vertices
        group_distance_matrix = [ [dist for w, dist in enumerate(distances) if w in group] for v, distances in enumerate(distance_matrix) if v in group ]

        # compute the list of requests for the stations in the group
        group_requests = [ r for station, r in enumerate(requests) if station + 1 in group ]

        problem = OnePDTSP(group_distance_matrix, group_requests, vehicle_capacity)

        solution = simulated_annealing(problem, hyperparameters)
        if solution is None:
            return None

        solutions.append(solution)

    # combine the OnePDTSP solutions into a SBRP solution
    final_solution = SBRP_Solution.construct_from_OnePDTSPs(solutions, groups, SBRP(distance_matrix, requests, vehicle_num, vehicle_capacity))

    return final_solution

# function only for degugging
def print_m(matrix):
    for line in matrix:
        print(line)
    print()

def solve_SBRP(coordinates, requests, vehicle_num, vehicle_capacity, hyperparameters):
    # compute the distance matrix
    distance_matrix = compute_distance_matrix(coordinates)
    # print_m(distance_matrix)  # <- for debugging only

    # create an instance of the problem
    problem = SBRP(distance_matrix, requests, vehicle_num, vehicle_capacity)

    solution = simulated_annealing(problem, hyperparameters)

    return solution

algorithms = {
    "1": {
        "algorithm": solve_SBRP,
        "description": "Static Bike Repositioning Problem - Simulated Annealing algorithm",
        "default_hyperparameters": {
            "initial_probability_threshold": 0.95,
            "alpha": 0.8,   # rate of change for temperature, should be within range (0.8, 0.99)
            "beta": 1.05,    # rate of change for phase length, should be > 1
            "min_temp_percentage": 0.01,   # used to determine the termination criterion, what percentage of the initial temperature is the minimum temperature
            "initial_phase_length": 10
        }
    },
    "2": {
        "algorithm": solve_multiple_OnePDTSP,
        "description": "multiple instances of One-Commodity Pickup-Delivery TSP - Simulated Annealing algorithm",
        "default_hyperparameters": {
            "initial_probability_threshold": 0.95,
            "alpha": 0.95,   # rate of change for temperature, should be within range (0.8, 0.99)
            "beta": 1.05,    # rate of change for phase length, should be > 1
            "min_temp_percentage": 0.005,   # used to determine the termination criterion, what percentage of the initial temperature is the minimum temperature
            "initial_phase_length": 10
        }
    }
}

def solve(coordinates, utilisation_data, vehicle_num, vehicle_capacity, algorithm = "1", hyperparameters = "default"):
    # compute the requests for all stations
    start_time = time.time()
    requests = compute_requests(utilisation_data, vehicle_capacity)
    end_time = time.time()
    requests_time = end_time - start_time

    # print(sum(requests))   # <- for debugging only

    # check if the problem is solvable
    if abs(sum(requests)) > (vehicle_num * vehicle_capacity):
        print("The problem cannot be solved. Increase the number of vehicles or their capacity")
        return None

    # choose the correct solution approach and set of hyperparameters
    solver = algorithms.get(algorithm).get("algorithm")
    if hyperparameters == "default":
        hyperparameters = algorithms.get(algorithm).get("default_hyperparameters")
    # # NOTE: if hyperparameters were given as an argument, they should be validated,
    # otherwise the SA code might break;
    # this is left for future development

    # run the appropriate solution approach
    start_time = time.time()
    solution = solver(coordinates, requests, vehicle_num, vehicle_capacity, hyperparameters)
    end_time = time.time()
    solution_time = end_time - start_time

    if solution is None:
        return None

    # return the results as a dictionary
    result = {
        "requests": requests,
        "requests_time": requests_time,
        "solution": list( zip(solution.get_initial_loads(), solution.vehicle_paths) ),
        "solution_time": solution_time,
        "cost": solution.cost,
        "total_time": requests_time + solution_time
    }

    return result
