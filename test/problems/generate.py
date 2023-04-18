#!/usr/bin/env python3.7

import sys, os, json, random
import xml.etree.ElementTree as ET

def get_stations_data(stations_file = "cycle_hire-stations.xml", k = "all"):
    root = ET.parse(stations_file).getroot()

    # keys = {
    #     "id": "id",
    #     "nbDocks": "capacity",
    #     "nbBikes": "inventory",
    #     "lat": "latitude",
    #     "long": "longitude"
    # }

    stations = []
    for child in root:
        s = { subchild.tag: subchild.text for subchild in child }
        stations.append(s)

    is_unavailable = lambda s: s.get("installed") == "false" or s.get("locked") == "true" or s.get("removalDate") is not None or s.get("temporary") == "true"

    # filter out out-of-order stations
    stations = [ s for s in stations if not is_unavailable(s) ]

    # select k random stations from the network if k was provided
    if k != "all" and isinstance(k, int) and k > 0:
        stations = random.sample(stations, k=k)

    # construct the final list
    final_stations = []
    for s in stations:
        final_s = {
            "id": int(s.get("id")),
            "capacity": int(s.get("nbDocks")),
            "inventory": int(s.get("nbBikes")),
            "latitude": float(s.get("lat")),
            "longitude": float(s.get("long"))
        }
        final_stations.append(final_s)

    return final_stations

def load_demand_files(demand_dir):
    demand_filenames = os.listdir(demand_dir)

    demand_files = []
    for filename in demand_filenames:
        try:
            with open(demand_dir + "/" + filename) as file:
                demand = json.load(file)

            demand_files.append(demand)
        except FileNotFoundError as e:
            print("Error: No such file: " + e.filename)
        except json.decoder.JSONDecodeError as e:
            print("Parsing error [line " + str(e.lineno) + "]: " + e.msg)

    return demand_files

def load_depot_specs(depot_file):
    try:
        with open(depot_file) as file:
            depot_specs = json.load(file)

        return depot_specs
    except FileNotFoundError as e:
        print("Error: No such file: " + e.filename)
        return None
    except json.decoder.JSONDecodeError as e:
        print("Parsing error [line " + str(e.lineno) + "]: " + e.msg)
        return None

def save_problem(problem, i, problem_dir):
    try:
        with open(problem_dir + "/problem" + str(i) + ".json", "w") as problem_file:
            json.dump(problem, problem_file, indent = "  ")
    except Exception as e:
        print("Unable to save the problem to a file [problem " + str(i) + "]")
        return None

def generate_problems(stations_file, depot_file, demand_dir, problem_dir, k):
    stations_list = get_stations_data(stations_file, k)

    demand_files = load_demand_files(demand_dir)

    final_stations_configs = []
    for demand in demand_files:
        updated_stations = []
        for station in stations_list:
            updated_s = station.copy()
            d = demand.get(str(updated_s.get("id")))
            if d is not None:
                updated_s["demand"] = d
                updated_stations.append(updated_s)
        final_stations_configs.append(updated_stations)

    depot = load_depot_specs(depot_file)

    # construct the problems
    num_vehicles_values = [40, 60, 80]#[1, 5, 10, 20]
    vehicle_capacity_values = [25, 35, 45]#[5, 10, 20]

    problems = []
    for num_vehicles in num_vehicles_values:
        for vehicle_capacity in vehicle_capacity_values:
            for stations_config in final_stations_configs:
                p = {
                    "vehicles": {
                        "number": num_vehicles,
                        "capacity": vehicle_capacity
                    },
                    "depot": depot,
                    "stations": stations_config
                }
                problems.append(p)

    index = 1
    for p in problems:
        save_problem(p, index, problem_dir)
        index += 1

if __name__ == '__main__':
    args = sys.argv

    stations_file = args[1]
    depot_file = args[2]
    demand_dir = args[3]
    problem_dir = args[4]

    k = "all"
    if len(args) > 5:
        k = int(args[5])

    # generate_problems(args[1], args[2], args[3], args[4], args[5] if args[5] is not None else "all")
    generate_problems(stations_file, depot_file, demand_dir, problem_dir, k)
