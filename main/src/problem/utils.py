import random

def depth_first_search(path, distance_matrix, requests, min_load, max_load, vehicle_capacity):
    if len(path) == len(distance_matrix):
        return path

    # NOTE: this comment contains an alternative version of the code below
    # # find reachable vertices
    # reachable = []
    # for index, request in enumerate(requests):
    #     vertex = index + 1
    #     min_required_load = max(0, 0 - request)
    #     max_required_load = min(vehicle_capacity, vehicle_capacity - request)
    #
    #     move_allowed = (min_load >= min_required_load and min_load <= max_required_load) or (max_load >= min_required_load and max_load <= max_required_load)
    #
    #     if vertex not in path and move_allowed:
    #         reachable.append(vertex)
    #
    # for vertex in reachable:
    #     request = requests[vertex - 1]
    #
    #     min_required_load = max(0, 0 - request)
    #     max_required_load = min(vehicle_capacity, vehicle_capacity - request)
    #
    #     # obtain the intersection of the two load ranges (available and required) as the new available range
    #     new_min_load = max(min_load, min_required_load) + request
    #     new_max_load = min(max_load, max_required_load) + request
    #
    #     final_path = depth_first_search(path + [vertex], distance_matrix, requests, new_min_load, new_max_load, vehicle_capacity)
    #     if final_path is not None:
    #         return final_path
    #
    # return None

    for index, request in enumerate(requests):
        vertex = index + 1
        min_required_load = max(0, 0 - request)
        max_required_load = min(vehicle_capacity, vehicle_capacity - request)

        move_allowed = (min_load >= min_required_load and min_load <= max_required_load) or (max_load >= min_required_load and max_load <= max_required_load)

        if vertex not in path and move_allowed:
            # obtain the intersection of the two load ranges (available and required) as the new available range
            new_min_load = max(min_load, min_required_load) + request
            new_max_load = min(max_load, max_required_load) + request

            final_path = depth_first_search(path + [vertex], distance_matrix, requests, new_min_load, new_max_load, vehicle_capacity)
            if final_path is not None:
                return final_path

    return None


def compute_assignment_cost(assignments, requests, vehicle_num, vehicle_capacity):
    # compute the net request for each group of stations
    net_requests = [ 0 for i in range(0, vehicle_num) ]
    for station, vehicle in enumerate(assignments):
        net_requests[vehicle] += requests[station]

    # compute the cost as the sum of outstanding requests for each vehicle
    # an outstanding request if defined as:
    #    abs(net_request) - vehicle_capacity,  if net_request not in [-vehicle_capacity, vehicle_capacity]
    #    0 otherwise
    cost = sum( [ max(0, abs(net_r) - vehicle_capacity) for net_r in net_requests ] )
    # cost = sum( [ abs(net_r) - vehicle_capacity for net_r in net_requests ] )

    return cost

def generate_initial_assignments(requests, vehicle_num):
    # compute the target net request for each vehicle
    avg_net_request = sum(requests) / vehicle_num

    net_requests = [ 0 for i in range(0, vehicle_num) ]

    assignments = []
    for r in requests:
        # for each vehicle compute the distance to target after the station is assigned to it
        target_dist = [ abs(avg_net_request - net_r - r) for net_r in net_requests ]

        # choose the assignment that reduces the distance the most
        vehicle_id = target_dist.index( min(target_dist) )

        # apply the assignment
        assignments.append(vehicle_id)
        net_requests[vehicle_id] += r

    return assignments

def generate_neighbour_assignment(assignments, vehicle_num):
    new_assignments = assignments.copy()    # we do not want to modify the original solution

    # choose a random station to be reassigned
    station, current_vehicle = random.choice( list(enumerate(assignments)) )

    # reassign the station to a random different vehicle
    new_assignments[station] = ( current_vehicle + random.randint(1, vehicle_num - 1) ) % vehicle_num

    return new_assignments

def tabu_search(requests, vehicle_num, vehicle_capacity):
    # assignments = [ random.randint(0, vehicle_num - 1) for i in range(0, len(requests)) ]
    assignments = generate_initial_assignments(requests, vehicle_num)
    cost = compute_assignment_cost(assignments, requests, vehicle_num, vehicle_capacity)

    stations_num = len(requests)
    visited = []
    visited_size_limit = stations_num

    # define the max number of iterations
    neighbourhood_size = stations_num * vehicle_num
    max_iterations = 2 * neighbourhood_size
    iter = 0

    # perform the search
    while cost > 0 and iter < max_iterations:
        new_assignments = generate_neighbour_assignment(assignments, vehicle_num)
        new_cost = compute_assignment_cost(new_assignments, requests, vehicle_num, vehicle_capacity)
        if str(new_assignments) not in visited:
            if new_cost <= cost:
                assignments = new_assignments
                cost = new_cost
            iter += 1
            visited.append( str(new_assignments) )
            if len(visited) > visited_size_limit:
                visited.pop(0)

    # return the solution if a valid one was found
    if cost <= 0:
        return assignments
    else:
        return None


def is_path_valid(path, requests):
    pass
