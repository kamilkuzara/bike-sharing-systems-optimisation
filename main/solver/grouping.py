from sklearn.cluster import KMeans

def is_grouping_valid(group_assignments, num_groups, requests, vehicle_capacity):
    group_requests = [ 0 for g in range(0, num_groups) ]

    for station, group in enumerate(group_assignments):
        group_requests[group] += requests[station]

    for net_request in group_requests:
        if abs(net_request) > vehicle_capacity:
            return False

    return True

def compute_score(group_assignments, num_groups, distance_matrix):
    groups = [ [] for g in range(0, num_groups) ]

    for station, group in enumerate(group_assignments):
        groups[group].append(station)

    score = 0
    for group in groups:
        # compute the distance matrix for the group of vertices
        group_distance_matrix = [ [dist for w, dist in enumerate(distances) if w in group] for v, distances in enumerate(distance_matrix) if v in group ]

        # flatten the matrix
        group_distances = [ dist for row in group_distance_matrix for dist in row ]

        # a useful distance is one between two different stations; as such we disregard
        # the distances that connect a station to itself;
        # there are len(group_distance_matrix) such distances
        num_useful_distances = len(group_distances) - len(group_distance_matrix)

        avg_dist = sum(group_distances) / num_useful_distances if num_useful_distances > 0 else 0

        score += avg_dist

    return score

def compute_station_groups(coordinates, distance_matrix, requests, vehicle_num, vehicle_capacity):
    best_assignments = None
    best_num_groups = 0
    best_score = 0

    max_groups = min( len(requests), vehicle_num )
    for num_groups in range(1, max_groups + 1):
        # create a kmeans classifier and compute the clusters/groups
        group_assignments = KMeans(n_clusters = num_groups).fit_predict(coordinates)

        # verify if the grouping is valid
        if is_grouping_valid(group_assignments, num_groups, requests, vehicle_capacity):
            current_score = compute_score(group_assignments, num_groups, distance_matrix)

            # check if best grouping yet or if first tested
            if best_assignments is None or current_score <= best_score:
                best_assignments = group_assignments
                best_num_groups = num_groups
                best_score = current_score

    return best_assignments, best_num_groups
