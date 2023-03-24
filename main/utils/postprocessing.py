def perform_postprocessing(result, id_mapping):
    r = {}

    requests = {}
    for id, request in enumerate(result.get("requests")):
        true_id = id_mapping[id + 1]
        # requests[str(true_id)] = request
        requests[true_id] = request
    r["requests"] = requests

    solution = {}
    for index, vehicle in enumerate(result.get("solution")):
        init_load, path = vehicle
        true_path = []
        for vertex in path:
            true_path.append(id_mapping[vertex])

        solution[ ("vehicle_" + str(index)) ] = {
            "initial_load": init_load,
            "route": true_path
        }
    r["solution"] = solution

    r["cost"] = result.get("cost")
    r["requests_time"] = result.get("requests_time")
    r["solution_time"] = result.get("solution_time")
    r["total_time"] = result.get("total_time")

    return r
