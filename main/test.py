#!/usr/bin/env python3.7

import sys
import os
import random
import multiprocessing

import utils
import solver

import pandas as pd

# #######################################################################
# The function parses command line parameters. It expects to receive an array
# where each item is a parameter. The 0-th item is the name of the program followed
# by parameters specified in the command line.
#
# @return dictionary with parameters if correct number of parameters, otherwise: None
#
def parse_args(argv):

    # array cannot be empty
    if len(argv) < 4:
        # raise Exception("Incorrect number of parameters\n" + utils.get_help())
        print("Incorrect number of parameters")
        return None

    args = {
        "problem_dir": argv[1],
        "solution_dir": argv[2],
        "stats_file": argv[3]
    }

    return args

def process_result(result, id_mapping, solution_dir, problem_name, algo, timed_out):
    solution_filename = solution_dir + problem_name + "-solution_" + algo + ".json"

    if result is None:
        res = {}
        if timed_out:
            res["timed_out"] = timed_out
        utils.save_to_file(res, solution_filename)
        return [None, None, None, None, None, timed_out]

    # construct a dictionary in the JSON format from the result
    result = utils.perform_postprocessing(result, id_mapping)
    utils.save_to_file(result, solution_filename)

    # compute the number of vehicles that perform the repositioning
    num_vehicles_used = 0
    for _, vehicle_specs in result.get("solution").items():
        route = vehicle_specs.get("route")
        if len(route) > 1:
            num_vehicles_used += 1

    cost = round(result.get("cost"), 3)
    requests_time = round(result.get("requests_time"), 3)
    solution_time = round(result.get("solution_time"), 3)
    total_time = round(result.get("total_time"), 3)

    return [num_vehicles_used, cost, requests_time, solution_time, total_time, timed_out]

def run_algorithm(coordinates, utilisation_data, vehicle_num, vehicle_capacity, algorithm, result):
    result["result"] = solver.solve(coordinates, utilisation_data, vehicle_num, vehicle_capacity, algorithm)

def test_single_algorithm(coordinates, utilisation_data, vehicle_num, vehicle_capacity, algorithm, algorithm_name):
    print("  " + algorithm_name + " - attempts: ", end="")
    # result = None
    manager = multiprocessing.Manager()
    result = manager.dict()
    num_attempts = 0
    timed_out = False
    while num_attempts < 2 and result.get("result") is None:
        print(num_attempts + 1, end = " ")
        p = multiprocessing.Process(target = run_algorithm, args = (coordinates, utilisation_data, vehicle_num, vehicle_capacity, algorithm, result))
        p.start()

        # wait for 5 minutes
        p.join(300)

        # terminate the function if it is still running
        if p.is_alive():
            p.terminate()
            p.join()
            timed_out = True
            print(" - timed out", end = " ")
        # result = solver.solve(coordinates, utilisation_data, vehicle_num, vehicle_capacity, algorithm)
        num_attempts += 1
    print( ("[solution found]" if result.get("result") is not None else "[fail]") )

    # return result, num_attempts, timed_out
    return result.get("result"), num_attempts, timed_out

def test_single_problem(problem_dir, filename, solution_dir):
    # load the problem specification
    problem_specs = utils.load_problem_specs(problem_dir + filename)
    if problem_specs is None:
        return None

    # validate the problem specification
    if not utils.is_valid(problem_specs):
        return None

    # perform preprocessing
    id_mapping, coordinates, utilisation_data = utils.perform_preprocessing(problem_specs)
    vehicle_num = problem_specs.get("vehicles").get("number")
    vehicle_capacity = problem_specs.get("vehicles").get("capacity")

    # test SA on SBRP
    result_SBRP, SBRP_num_attempts, SBRP_timed_out = test_single_algorithm(coordinates, utilisation_data, vehicle_num, vehicle_capacity, "1", "SBRP")

    # test SA on multiple OnePDTSPs
    result_OnePDTSP, OnePDTSP_num_attempts, OnePDTSP_timed_out = test_single_algorithm(coordinates, utilisation_data, vehicle_num, vehicle_capacity, "2", "OnePDTSP")

    # print("  OnePDTSP - attempts: ", end="")
    # result_OnePDTSP = None
    # OnePDTSP_num_attempts = 0
    # while OnePDTSP_num_attempts < 2 and result_OnePDTSP is None:
    #     print(OnePDTSP_num_attempts + 1, end=" ")
    #     result_OnePDTSP = solver.solve(coordinates, utilisation_data, vehicle_num, vehicle_capacity, algorithm = "2")
    #     OnePDTSP_num_attempts += 1
    # print( ("[solution found]" if result_OnePDTSP is not None else "[fail]") )

    problem_name = filename[:len(filename) - 5]
    stats_SBRP = process_result(result_SBRP, id_mapping, solution_dir, problem_name, "SBRP", SBRP_timed_out)
    stats_OnePDTSP = process_result(result_OnePDTSP, id_mapping, solution_dir, problem_name, "OnePDTSP", OnePDTSP_timed_out)

    stations_num = len(coordinates) - 1

    return [problem_name, stations_num, vehicle_num, vehicle_capacity] + [SBRP_num_attempts] + stats_SBRP + [OnePDTSP_num_attempts] + stats_OnePDTSP

def main():
    # # parse command-line arguments
    args = parse_args(sys.argv)
    if args is None:
        return

    stats_df = pd.DataFrame(columns=["problem_name", "stations_num", "vehicle_num", "vehicle_capacity",
    "SBRP_num_attempts", "SBRP_num_vehicles_used", "SBRP_cost", "SBRP_requests_time", "SBRP_solution_time", "SBRP_total_time", "SBRP_timed_out",
    "OnePDTSP_num_attempts", "OnePDTSP_num_vehicles_used", "OnePDTSP_cost", "OnePDTSP_requests_time", "OnePDTSP_solution_time", "OnePDTSP_total_time", "OnePDTSP_timed_out"])

    problem_dir = args.get("problem_dir") + "/" #"../test/problems/"
    problem_files = sorted(os.listdir(problem_dir))

    solution_dir = args.get("solution_dir") + "/" #"../test/solutions/"

    for filename in problem_files:
        print("Testing: " + filename)
        problem_row = test_single_problem(problem_dir, filename, solution_dir)
        stats_df.loc[len(stats_df)] = problem_row
        print("--------------------------")

    # replace all the None values with "-"
    stats_df = stats_df.fillna("-")

    # save stats to a CSV file
    stats_file = args.get("stats_file")
    # stats_df.to_csv("../test/stats.csv")
    stats_df.to_csv(stats_file)


if __name__ == '__main__':
    main()
