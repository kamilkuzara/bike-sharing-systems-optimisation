import json
from .utils import get_help

# #######################################################################
# Open and parse the problem file. The problem file has to be in JSON format.
# A python dictionary is constructed from the JSON file.
#
# @param problem_file_path path to the problem file
# @return dictionary with problem specification if problem file parsed correctly, otherwise: None
#
def load_problem_specs(problem_file_path):
    try:
        with open(problem_file_path) as problem_file:
            problem_specs = json.load(problem_file)

        return problem_specs
    except FileNotFoundError as e:
        print("Error: No such file: " + e.filename + "\n\n" + get_help())
        return None
    except json.decoder.JSONDecodeError as e:
        print("Parsing error [line " + str(e.lineno) + "]: " + e.msg + "\n\n" + get_help())
        return None

def save_to_file(result, filename):
    try:
        with open(filename, "w") as solution_file:
            json.dump(result, solution_file, indent = "  ")
    except Exception as e:
        print("Unable to save the solution to a file")
        return None
