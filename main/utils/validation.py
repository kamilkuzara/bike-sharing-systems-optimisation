error_message = "Error: Invalid problem specification. "

def has_valid_integer_key(object, key):
    # must contain the key and its value must be a positive integer
    key_missing = key not in object
    value = object.get(key)
    invalid_type = not isinstance(value, int)

    if key_missing or invalid_type:
        return False

    if value <= 0:
        return False

    return True

def vehicles_valid(vehicle_specs):
    # must be a dictionary
    if not isinstance(vehicle_specs, dict):
        print(error_message + "Invalid vehicle specification")
        return False

    # must contain a valid number of vehicles
    if not has_valid_integer_key(vehicle_specs, "number"):
        print(error_message + "Number of vehicles not specified or not a positive integer")
        return False

    # must contain a valid vehicle capacity
    if not has_valid_integer_key(vehicle_specs, "capacity"):
        print(error_message + "Vehicle capacity not specified or not a positive integer")
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

def has_valid_coordinates(vertex):
    if not has_valid_latitude(vertex) or not has_valid_longitude(vertex):
        print(error_message + "The coordinates of a vertex are missing or invalid")
        return False

    return True

def has_valid_id(vertex, used_ids):
    # must contain the id of the vertex and the id must be an integer
    id_missing = "id" not in vertex
    invalid_id_type = not isinstance(vertex.get("id"), int)
    if id_missing or invalid_id_type:
        print(error_message + "ID of a vertex not specified or not an integer")
        return False

    # id must be unique
    is_unique = vertex.get("id") not in used_ids

    if not is_unique:
        print(error_message + "Each vertex ID must be unique")
        return False

    return True

def depot_valid(depot_specs, used_ids = set()):
    # must be a dictionary
    if not isinstance(depot_specs, dict):
        print(error_message + "Invalid depot specification")
        return False

    if not has_valid_id(depot_specs, used_ids):
        return False

    if not has_valid_coordinates(depot_specs):
        return False

    return True

def has_valid_inventory(station, capacity):
    # must contain the key and its value must be an integer
    invalid = not isinstance(station.get("inventory"), int)

    if invalid:
        print(error_message + "Inventory of a station not specified or not an integer")
        return False

    inventory = station.get("inventory")
    if inventory > capacity or inventory < 0:
        print(error_message + "Station inventory cannot be less than 0 or greater than station capacity")
        return False

    return True

def has_valid_demand(station, demand_array_len):
    # demand_missing = "demand" not in station  # <- redundant
    demand = station.get("demand")
    invalid_or_missing = not isinstance(demand, dict)

    if invalid_or_missing:
        print(error_message + "Demand of a station not specified or invalid")
        return False

    pickups = demand.get("pickups")
    pickups_valid = isinstance(pickups, list)

    returns = demand.get("returns")
    returns_valid = isinstance(returns, list)

    if not pickups_valid or not returns_valid:
        print(error_message + "Demand specification is incomplete or invalid")
        return False

    if len(pickups) == 0 or len(returns) == 0:
        print(error_message + "'pickups' and 'returns' arrays cannot be empty")
        return False

    if len(pickups) != len(returns):
        print(error_message + "'pickups' and 'returns' arrays have to be of the same length")
        return False

    if demand_array_len != None and len(pickups) != demand_array_len:
        print(error_message + "Demand for all stations has to be specified with arrays of the same length")
        return False

    # check if pickups and returns contain only non-negative integers
    for p, r in zip(pickups, returns):
        if not isinstance(p, int) or not isinstance(r, int):
            print(error_message + "'pickups' and 'returns' arrays must contain only non-negative integer values")
            return False

        if p < 0 or r < 0 :
            print(error_message + "'pickups' and 'returns' arrays must contain only non-negative integer values")
            return False

    return True

def is_station_valid(station, used_ids, demand_array_len):
    # must be a dictionary
    if not isinstance(station, dict):
        print(error_message + "Invalid station specification")
        return False

    # check if id valid, i.e. a unique integer
    if not has_valid_id(station, used_ids):
        return False

    # check if coordinates valid
    if not has_valid_coordinates(station):
        return False

    # check if capacity is valid
    if not has_valid_integer_key(station, "capacity"):
        # print(error_message + "Capacity of a station not specified or not a positive integer [station ID: " + station.get("id") + "]")
        print(error_message + "Capacity of a station not specified or not a positive integer")
        return False

    # check if inventory is valid, i.e. a non-negative integer less than or equal to capacity
    if not has_valid_inventory(station, station.get("capacity")):
        # print(station)    # <- for debugging only
        return False

    # check if demand is valid
    if not has_valid_demand(station, demand_array_len):
        return False

    return True

def stations_valid(stations_specs, used_ids = set()):
    # must be a list
    if not isinstance(stations_specs, list):
        print(error_message + "Stations must be given as a list")
        return False

    # the list cannot be empty
    if len(stations_specs) == 0:
        print(error_message + "The list of stations cannot be empty")
        return False

    # validate each of the stations in the list
    demand_array_len = None
    for station in stations_specs:
        if not is_station_valid(station, used_ids, demand_array_len):
            return False

        used_ids.add(station.get("id"))
        if demand_array_len == None:
            demand_array_len = len(station.get("demand").get("pickups"))

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

    if not stations_valid(problem_specs.get("stations"), { problem_specs.get("depot").get("id") }):
        return False

    return True
