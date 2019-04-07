import numpy as np
from .struct import Graph, Node


def _euclidean_dist(p1, p2):
    return np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


# Given three colinear points p, q, r,checks if q lies on line segment 'pr'
def _on_segment(p, q, r):
    return q[0] <= max(p[0], r[0]) and q[0] >= min(p[0], r[0]) and \
        q[1] <= max(p[1], r[1]) and q[1] >= min(p[1], r[1])


# To find the orientation of an ordered triplet (p, q, r).
# Returns:
#  0 --> p, q and r are colinear
#  1 --> Clockwise
# -1 --> Counterclockwise
def _orientation(p, q, r):
    aux = (q[1] - p[1]) * (r[0] - q[0]) - \
        (q[0] - p[0]) * (r[1] - q[1])

    if aux == 0:
        return 0

    return 1 if aux > 0 else -1


# Basic idea taken from
# https://www.geeksforgeeks.org/check-if-two-given-line-segments-intersect/
def _lines_cross(p1, q1, p2,  q2):
    o1 = _orientation(p1, q1, p2)
    o2 = _orientation(p1, q1, q2)
    o3 = _orientation(p2, q2, p1)
    o4 = _orientation(p2, q2, q1)

    # General case
    if o1 != o2 and o3 != o4:
        return True

    # Special cases:
    # p1, q1, and p2 are colinear and p2 lies in p1q1
    if o1 == 0 and _on_segment(p1, p2, q1):
        return True

    # p1, q1, and q2 are colinear and q2 lies in p1q1
    if o2 == 0 and _on_segment(p1, q2, q1):
        return True

    # p2, q2, and p1 are colinear and p1 lies in p2q2
    if o3 == 0 and _on_segment(p2, p1, q2):
        return True

    # p2, q2, and q1 are colinear and q1 lies in p2q2
    if o4 == 0 and _on_segment(p2, q1, q2):
        return True

    return False


def _argmin_connection(i, coordinates, connected):
    dists = [
        _euclidean_dist(coordinates[i], coordinates[j]) if j != i else
        float('Inf') for j in range(len(coordinates))
    ]

    j = np.argmin(dists)

    if (coordinates[i], coordinates[j]) not in connected:
        if len(connected) == 0:
            return (coordinates[i], coordinates[j])

        intersect = [
            _lines_cross(
                coordinates[i], coordinates[j],
                p, q
            ) for p, q in connected
        ]

        if not any(intersect):
            return (coordinates[i], coordinates[j])

    return None


def random_map_coloring(n_points):
    x = np.random.uniform(size=n_points)
    y = np.random.uniform(size=n_points)

    coordinates = [(i, j) for i, j in zip(x, y)]
    connected = set()

    # TODO verify stopping criteria and build graph
