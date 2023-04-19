#!/usr/bin/env python3.7

import sys
import os
import json
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
    if len(argv) < 5:
        # raise Exception("Incorrect number of parameters\n" + utils.get_help())
        print("Incorrect number of parameters")
        return None

    args = {
        "hyperparameters_dir": argv[1],
        "problem_dir": argv[2],
        "solution_dir": argv[3],
        "stats_file": argv[4]
    }

    return args

def process_result(result, id_mapping, solution_dir, problem_name, algo, hyperparameters_filename, timed_out):
    solution_filename = solution_dir + hyperparameters_filename + "-" + problem_name + "-solution_" + algo + ".json"

    if result is None:
        res = {}
        if timed_out:
            res["timed_out"] = timed_out
        utils.save_to_file(res, solution_filename)
        return [None, None, timed_out]

    # construct a dictionary in the JSON format from the result
    result = utils.perform_postprocessing(result, id_mapping)
    utils.save_to_file(result, solution_filename)

    cost = round(result.get("cost"), 3)
    solution_time = round(result.get("solution_time"), 3)

    return [cost, solution_time, timed_out]

def run_algorithm(coordinates, utilisation_data, vehicle_num, vehicle_capacity, algorithm, hyperparameters, result):
    result["result"] = solver.solve(coordinates, utilisation_data, vehicle_num, vehicle_capacity, algorithm, hyperparameters)

def test_single_algorithm(coordinates, utilisation_data, vehicle_num, vehicle_capacity, algorithm, algorithm_name, hyperparameters):
    print("    " + algorithm_name + " - attempts: ", end="")
    # result = None
    result = {}
    num_attempts = 0
    timed_out = False
    while num_attempts < 2 and result.get("result") is None:
        print(num_attempts + 1, end = " ")
        # p = multiprocessing.Process(target = solver.solve, args = (coordinates, utilisation_data, vehicle_num, vehicle_capacity, algorithm, hyperparameters))
        p = multiprocessing.Process(target = run_algorithm, args = (coordinates, utilisation_data, vehicle_num, vehicle_capacity, algorithm, hyperparameters, result))
        p.start()

        # wait for 5 minutes
        p.join(300)

        # terminate the function if it is still running
        if p.is_alive():
            p.terminate()
            p.join()
            timed_out = True
            print(" - timed out", end = " ")
        # result = solver.solve(coordinates, utilisation_data, vehicle_num, vehicle_capacity, algorithm, hyperparameters)
        num_attempts += 1
    print( ("[solution found]" if result.get("result") is not None else "[fail]") )

    # return result, num_attempts, timed_out
    return result.get("result"), num_attempts, timed_out

def test_single_problem(hyperparameters_filename, hyperparameters, problem_dir, filename, solution_dir):
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
    result_SBRP, SBRP_num_attempts, SBRP_timed_out = test_single_algorithm(coordinates, utilisation_data, vehicle_num, vehicle_capacity, "1", "SBRP", hyperparameters)

    # test SA on multiple OnePDTSPs
    result_OnePDTSP, OnePDTSP_num_attempts, OnePDTSP_timed_out = test_single_algorithm(coordinates, utilisation_data, vehicle_num, vehicle_capacity, "2", "OnePDTSP", hyperparameters)

    problem_name = filename[:len(filename) - 5]
    stats_SBRP = process_result(result_SBRP, id_mapping, solution_dir, problem_name, "SBRP", hyperparameters_filename[:len(hyperparameters_filename) - 5], SBRP_timed_out)
    stats_OnePDTSP = process_result(result_OnePDTSP, id_mapping, solution_dir, problem_name, "OnePDTSP", hyperparameters_filename[:len(hyperparameters_filename) - 5], OnePDTSP_timed_out)

    return [problem_name] + [SBRP_num_attempts] + stats_SBRP + [OnePDTSP_num_attempts] + stats_OnePDTSP

def test_hyperparameter_set(stats_df, hyperparameters_dir, hyperparameters_file, problem_dir, problem_files, solution_dir):
    try:
        # open the hyperparameters file
        with open(hyperparameters_dir + hyperparameters_file) as file:
            hyperparameters = json.load(file)

        print("Testing: " + hyperparameters_file)
        for filename in problem_files:
            print("  " + filename + ":")
            problem_row = test_single_problem(hyperparameters_file, hyperparameters, problem_dir, filename, solution_dir)
            stats_df.loc[len(stats_df)] = [hyperparameters_file] + problem_row

        print("--------------------------")

        return stats_df
    except FileNotFoundError as e:
        print("Error: No such file: " + e.filename)
        return stats_df
    except json.decoder.JSONDecodeError as e:
        print("Parsing error [line " + str(e.lineno) + "]: " + e.msg)
        return stats_df

def main():
    # # parse command-line arguments
    args = parse_args(sys.argv)
    if args is None:
        return

    stats_df = pd.DataFrame(columns=["hyperparameters_file", "problem_name",
    "SBRP_num_attempts", "SBRP_cost", "SBRP_solution_time", "SBRP_timed_out",
    "OnePDTSP_num_attempts", "OnePDTSP_cost", "OnePDTSP_solution_time", "OnePDTSP_timed_out"])

    problem_dir = args.get("problem_dir") + "/" #"../test/problems/"
    # problem_files = ["problem13.json", "problem17.json", "problem21.json"]
    problem_files = [ filename for filename in os.listdir(problem_dir) if filename[len(filename) - 5:] == ".json" ]

    # select 3 random problems
    random.seed(0)
    problem_files = random.sample(problem_files, k = 3)
    print("Selected problem files: ", problem_files)
    print()

    solution_dir = args.get("solution_dir") + "/" #"../test/solutions/"

    hyperparameters_dir = args.get("hyperparameters_dir") + "/"
    hyperparameter_files = sorted(os.listdir(hyperparameters_dir))
    hyperparameter_files = [ file for file in hyperparameter_files if file[len(file) - 5:] == ".json" ]

    for file in hyperparameter_files:
        stats_df = test_hyperparameter_set(stats_df, hyperparameters_dir, file, problem_dir, problem_files, solution_dir)

    # replace all the None values with "-"
    stats_df = stats_df.fillna("-")

    # save stats to a CSV file
    stats_file = args.get("stats_file")
    # stats_df.to_csv("../test/stats.csv")
    stats_df.to_csv(stats_file)


if __name__ == '__main__':
    main()
