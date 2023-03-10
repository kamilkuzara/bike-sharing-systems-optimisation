from solver import algorithms

def get_help():
    help_text = "Usage: python3.7 main.py  <problem_file>  [solution_method]  [solution_file]\n\n"
    help_text += "Available solution methods:\n"

    for algorithm_code, algorithm in algorithms.items():
        help_text += "\t" + algorithm_code + " - " + algorithm.get("description", "No description provided or out-of-use. See the documentation for details") + "\n"

    return help_text
