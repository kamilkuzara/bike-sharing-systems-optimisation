from solver import algorithms

def get_help():
    help_text = "Usage: python3.7 main.py  <problem_file>  [solution_method]  [solution_file]\n\n"
    help_text += "Available solution methods:\n"

    for algorithm_code, algorithm in algorithms.items():
        help_text += "\t" + algorithm_code + " - " + algorithm.get("description", "No description provided or out-of-use. See the documentation for details") + "\n"

    return help_text

def stringify_result(result):
    output = ""

    requests_string_data = []
    for station, request in result.get("requests").items():
        station_string = str(station)
        request_string = str(request)
        station_len = len(station_string)
        request_len = len(request_string)

        if station_len < request_len:
            station_string = (" " * (request_len - station_len)) + station_string
        elif station_len > request_len:
            request_string = (" " * (station_len - request_len)) + request_string

        requests_string_data.append( (station_string, request_string) )

    output += "Requests:\n"
    output += "  station: "
    for station, _ in requests_string_data:
        output += station + " "
    output += "\n"
    output += "  request: "
    for _, request in requests_string_data:
        output += request + " "
    output += "\n\n"

    output += "Solution:\n"
    for vehicle, specs in result.get("solution").items():
        output += "  " + vehicle + " [" + str(specs.get("initial_load")) + "]: "
        output += str(specs.get("route"))
        output += "\n"
    output += "\n"

    output += "Cost: " + str(result.get("cost")) + "\n\n"

    output += "Computation time:\n"
    output += "  requests: " + str(result.get("requests_time")) + " sec\n"
    output += "  solution: " + str(result.get("solution_time")) + " sec\n"
    output += "  total: " + str(result.get("total_time")) + " sec\n"

    return output
