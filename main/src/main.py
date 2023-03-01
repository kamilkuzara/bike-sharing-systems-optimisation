#!/usr/bin/env python3

import sys
import utils
# import algorithms


# #######################################################################
# The function parses command line parameters. It expects to receive an array
# where each item is a parameter. The 0-th item is the name of the program followed
# by parameters specified in the command line.
#
# @return dictionary with parameters if correct number of parameters, otherwise: None
#
def parse_args(argv):

    # array cannot be empty
    if len(argv) == 0:
        # raise Exception("Incorrect number of parameters\n" + utils.get_help())
        print("Incorrect number of parameters\n" + utils.get_help())
        return None

    # the user did not provide any parameters
    if len(argv) == 1:
        # raise Exception(utils.get_help())
        print(utils.get_help())
        return None

    # NOTE: This snippet of code was left here in case the minimum number of parameters increases in the future
    # # the user specified some params but not enough to continue execution
    # if len(argv) < 2:
    #     # raise Exception("Parameters missing\n" + utils.get_help())
    #     print("Parameters missing\n" + utils.get_help())
    #     return None

    # if we get here, required no. of params satisfied

    params = {
        "problem_file_path": argv[1]
    }

    # parse optional arguments if provided

    if len(argv) >= 3:
        # parse algorithm code
        algo = argv[2]
        if algo not in algorithms.algorithms:
            # raise Exception("Incorrect algorithm code\n" + utils.get_help())
            print("Incorrect algorithm code\n" + utils.get_help())
            return None

        params["algorithm_code"] = algo

    if len(argv) >= 4:
        params["solution_file_path"] = argv[3]

    return params

def main():
    # 1. parse arguments from the command line <- DONE
    # 2. load the problem from file <- DONE
    # 3. validate input data (e.g. no two nodes can have the same id, etc.) <- DONE
    # 4. preprocess the data <- DONE
    #   ( i.e. create appropriate data structs for algorithms, a mapping array from ids to [0..n] )
    # 5. call chosen algorithm with the problem instance
    # 6. validate the solution
    #   NOTE: this step should not be necessary as local search maintains a complete
    #   and valid at all times
    # 7. (optional) save solution to a file

    # parse command-line arguments
    args = parse_args(sys.argv)
    if args is None:
        return

    # load the problem specification
    problem_specs = utils.load_problem_specs(args.get("problem_file_path"))
    if problem_specs is None:
        return

    # print(problem_specs)  # <- for debugging only

    # validate the problem specification
    if not utils.is_valid(problem_specs):
        return

    # print("Problem specification valid")    # <- for debugging only

    # perform preprocessing
    id_mapping, coordinates, utilisation_data = utils.perform_preprocessing(problem_specs)
    vehicle_num = problem_specs.get("vehicles").get("number")
    vehicle_capacity = problem_specs.get("vehicles").get("capacity")

    print(id_mapping)
    print("-------------------")
    print(coordinates)
    print("-------------------")
    print(utilisation_data)
    print("-------------------")
    print(str(vehicle_num) + "     " + str(vehicle_capacity))

    # try:
    #
    #     # create appropriate data structures from the parsed problem instance
    #     print("Performing preprocessing...\t", end = "")
    #     employees_df, tasks_df, gains = utils.perform_preprocessing(employees, tasks)
    #     print("Done")
    #     print(employees_df)
    #     print(tasks_df)
    #     print(gains)
    #
    #     # solve the problem instance
    #     print("\nRunning " + algorithms.algorithms[ args["algorithm"] ]["description"] + "...\t", end = "")
    #     result = algorithms.algorithms[ args["algorithm"] ][ "algorithm" ](employees_df, tasks_df, gains)
    #     print("Done (solution found)")
    #
    #     # validate the solution; if invalid, an exception will be raised
    #     print("Validating the solution...\t", end = "")
    #     utils.validate_solution( result["solution"] )
    #     print("Done (solution valid)")
    #
    #     # if we get here, the solution is valid
    #
    #     # print out the solution
    #     print("Solution:\n")
    #     print( utils.solution_to_string( result["solution"] ) )
    #
    #     # compute the statistics
    #     net_profit = utils.compute_net_profit( [ task for task in tasks if task["name"] in tasks_df.index ], result["total gain"] )
    #
    #     # print out the statistics
    #     print("Total gain: " + str(result["total gain"]) )
    #     print("Net profit: " + str(net_profit) )
    #     print("Running time: " + str( round(result["running time"], 5) ) + "sec")
    #
    # except Exception as e:
    #     print("\n")
    #     print(e)

if __name__ == '__main__':
    main()
