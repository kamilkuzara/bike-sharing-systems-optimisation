import time
import random

# WARNING: the funcion modifies the following arguments: inventories
# if these objects need to remain unchanged after the function terminates the function
# ought to be invoked with copies of those objects, i.e. inventories.copy()
def simulate_demand_realisation(capacity, inventories, pickups, returns):
    lost_demand = [0] * len(inventories)

    for p, r in zip(pickups, returns):
        pickup_probability = p / (p + r)
        while p + r > 0:
            # choose whether a pickup or a return is attempted
            action = 0
            if p > 0 and (random.random() <= pickup_probability or r <= 0):   # a pickup is attempted
                action = -1
                p -= 1
            else:   # a return is attempted
                action = 1
                r -= 1

            # attempt to apply the chosen action to the inventories
            for index, current_inventory in enumerate(inventories):
                updated_inventory = current_inventory + action
                if updated_inventory >= 0 and updated_inventory <= capacity:    # bike successfuly collected or returned
                    inventories[index] = updated_inventory
                else:   # station empty/full, bike could not be collected/returned
                    lost_demand[index] += 1

    return lost_demand

def compute_station_request(station_utilisation, max_request):
    capacity, current_inventory, pickups, returns = station_utilisation

    # compute the valid range of inventories
    length_left = min(current_inventory, max_request)
    length_right = min(capacity - current_inventory, max_request)
    valid_inventories = list( range(current_inventory - length_left, current_inventory + length_right + 1) )

    lost_demand = simulate_demand_realisation(capacity, valid_inventories, pickups, returns)

    # choose the inventory level with the minimum lost demand and compute the request as the difference with the current inventory:
    # request = current_inventory - ( current_inventory - length_left + lost_demand.index( min(lost_demand) ) )
    # which is equivalent to:
    return length_left - lost_demand.index( min(lost_demand) )

def compute_requests(utilisation_data, max_request):
    requests = []

    for station_utilisation in utilisation_data:
        station_request = compute_station_request(station_utilisation, max_request)
        requests.append(station_request)

    return requests

def solve(coordinates, utilisation_data, vehicle_num, vehicle_capacity, algorithm = "simulated_annealing_on_SBRP"):
    # compute the requests for all stations
    start_time = time.time()
    requests = compute_requests(utilisation_data, vehicle_capacity)
    end_time = time.time()
    requests_computation_time = end_time - start_time

    # print(requests)   # <- for debugging only

    # check if the problem is solvable
    if abs(sum(requests)) > (vehicle_num * vehicle_capacity):
        print("The problem cannot be solved. Increase the number of vehicles or their capacity")
        return None # TODO: need to rethink if None should be returned here

    # TODO:
    # - choose the appropriate algorithm
