error_message = "Error: Invalid problem specification. "

def vehicles_valid(vehicle_specs):
    # must be a dictionary
    if not isinstance(vehicle_specs, dict):
        print(error_message + "Invalid vehicle specification")
        return False

    # must contain the number of vehicles and the number must be a positive integer
    number_missing = "number" not in vehicle_specs
    vehicles_number = vehicle_specs.get("number")
    invalid_number_type = not isinstance(vehicles_number, int)

    if number_missing or invalid_number_type:
        print(error_message + "Number of vehicles not specified or not an integer")
        return False

    if vehicles_number <= 0:
        print(error_message + "Number of vehicles must be greater than 0")
        return False

    # must contain the capacity of vehicles and the capacity must be a positive integer
    capacity_missing = "capacity" not in vehicle_specs
    capacity = vehicle_specs.get("capacity")
    invalid_capacity_type = not isinstance(capacity, int)

    if capacity_missing or invalid_capacity_type:
        print(error_message + "Vehicle capacity not specified or not an integer")
        return False

    if capacity <= 0:
        print(error_message + "Vehicle capacity must be greater than 0")
        return False

    return True

def has_valid_latitude(node_specs):
    key = "latitude"
    lat = node_specs.get(key)

    key_missing = key not in node_specs
    invalid_type = (not isinstance(lat, float)) and (not isinstance(lat, int))

    if key_missing or invalid_type:
        return False

    invalid_range = (lat < -90) or (lat > 90)

    if invalid_range:
        return False

    return True

def has_valid_longitude(node_specs):
    key = "longitude"
    long = node_specs.get(key)

    key_missing = key not in node_specs
    invalid_type = (not isinstance(long, float)) and (not isinstance(long, int))

    if key_missing or invalid_type:
        return False

    invalid_range = (long < -180) or (long > 180)

    if invalid_range:
        return False

    return True

def depot_valid(depot_specs):
    # must be a dictionary
    if not isinstance(depot_specs, dict):
        print(error_message + "Invalid depot specification")
        return False

    # must contain the id of the depot and the id must be an integer
    id_missing = "id" not in depot_specs
    invalid_id_type = not isinstance(depot_specs.get("id"), int)
    if id_missing or invalid_id_type:
        print(error_message + "ID of the depot not specified or not an integer")
        return False

    if not has_valid_latitude(depot_specs) or not has_valid_longitude(depot_specs):
        print(error_message + "The coordinates of the depot are missing or invalid")
        return False

    return True

def stations_valid(stations_specs):
    return True

# Check if the file does not violate the requirements of the problem.
# Specifically:
#   - all required keys and "sub-keys" must be present (e.g. "vehicles", "depot", "stations", etc.)
#   - station IDs must be unique
#
# @param: problem_specs A Python dictionary containing the problem instance specification.
def is_valid(problem_specs):
    if "vehicles" not in problem_specs:
        print(error_message + "Vehicle parameters missing")
        return False

    if not vehicles_valid(problem_specs.get("vehicles")):
        return False

    if "depot" not in problem_specs:
        print(error_message + "Depot parameters missing")
        return False

    if not depot_valid(problem_specs.get("depot")):
        return False

    if "stations" not in problem_specs:
        print(error_message + "Stations not specified")
        return False

    if not stations_valid(problem_specs.get("stations")):
        return False

    # check if depot ID is different than all the station IDs

    return True
