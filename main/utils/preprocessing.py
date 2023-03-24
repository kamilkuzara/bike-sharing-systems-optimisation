def perform_preprocessing(problem_specs):
    id_mapping = []
    coordinates = []
    utilisation_data = []

    # map the id of the depot to the 0-th index of the problem data structures
    id_mapping.append(problem_specs.get("depot").get("id"))

    # add the coordinates of the depot to the list
    depot_latitude = problem_specs.get("depot").get("latitude")
    depot_longitude = problem_specs.get("depot").get("longitude")
    coordinates.append( (depot_latitude, depot_longitude) )

    # perform the preprocessing for the stations
    for station in problem_specs.get("stations"):
        # map the id of the station to an index
        id_mapping.append(station.get("id"))

        # add the coordinates of the station to the list
        station_latitude = station.get("latitude")
        station_longitude = station.get("longitude")
        coordinates.append( (station_latitude, station_longitude) )

        # repackage the utilisation data of the station (i.e. its current state and the demand)
        # into a 4-tuple and add it to the list
        station_capacity = station.get("capacity")
        station_inventory = station.get("inventory")
        pickups = station.get("demand").get("pickups")
        returns = station.get("demand").get("returns")
        utilisation_data.append( (station_capacity, station_inventory, pickups, returns) )

    return id_mapping, coordinates, utilisation_data
