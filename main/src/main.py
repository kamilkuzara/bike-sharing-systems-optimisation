#!/usr/bin/env python3.7

import sys
import utils
import solver


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
        if algo not in solver.algorithms:
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

    # for debugging only:
    # print(id_mapping)
    # print("-------------------")
    # print(coordinates)
    # print("-------------------")
    # print(utilisation_data)
    # print("-------------------")
    # print(str(vehicle_num) + "     " + str(vehicle_capacity))

    result = solver.solve(coordinates, utilisation_data, vehicle_num, vehicle_capacity, algorithm = args.get("algorithm_code", "1"))


if __name__ == '__main__':
    main()
