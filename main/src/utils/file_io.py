import json
from .help import get_help

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
