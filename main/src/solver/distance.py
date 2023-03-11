import geopy.distance


def compute_distance_matrix(coordinates):
    matrix_size = len(coordinates)
    distance_matrix = [ [ 0 for col in range(0, matrix_size) ] for row in range(0, matrix_size) ]

    for i in range(0, matrix_size - 1):
        coordinates_i = coordinates[i]
        for j in range(i + 1, matrix_size):
            coordinates_j = coordinates[j]

            # calculate the distance between the two points (in meters)
            dist = geopy.distance.geodesic(coordinates_i, coordinates_j).m

            # update the relevant entries in the distance matrix
            distance_matrix[i][j] = dist
            distance_matrix[j][i] = dist

    return distance_matrix
