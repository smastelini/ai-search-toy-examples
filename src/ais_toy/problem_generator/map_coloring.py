import numpy as np


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


def _lines_cross2(p1, q1, p2,  q2):
    m1 = (q1[1] - p1[1])/(q1[0] - p1[0])
    m2 = (q2[1] - p2[1])/(q2[0] - p2[0])

    if np.isclose(m1, m2):
        return False

    b1 = p1[1] - m1 * p1[0]
    b2 = p2[1] - m2 * p2[0]

    x = (b2 - b1)/(m1 - m2)
    y = m1 * (x - p1[0]) + p1[1]

    if x > min(p1[0], q1[0]) and x > min(p2[0], q2[0]) and \
            x < max(p1[0], q1[0]) and x < max(p2[0], q2[0]) and \
            y > min(p1[1], q1[1]) and y > min(p2[1], q2[1]) and \
            y < max(p1[1], q1[1]) and y < max(p2[1], q2[1]):
        return True

    return False


def _argmin_connection(i, coordinates, connected):
    dists = [
        _euclidean_dist(coordinates[i], coordinates[j]) if j != i else
        float('Inf') for j in range(len(coordinates))
    ]

    for j in range(len(coordinates)):
        if (i, j) in connected or (j, i) in connected:
            dists[j] = float('Inf')

    while True:
        j = np.argmin(dists)

        if not np.isfinite(dists[j]):
            return None

        if len(connected) == 0:
            return (i, j)

        intersect = []
        for p, q in connected:
            if coordinates[i][0] < coordinates[j][0]:
                p1 = coordinates[i]
                q1 = coordinates[j]
            else:
                p1 = coordinates[j]
                q1 = coordinates[i]

            if coordinates[p][0] < coordinates[q][0]:
                p2 = coordinates[p]
                q2 = coordinates[q]
            else:
                p2 = coordinates[q]
                q2 = coordinates[p]

            intersect.append(_lines_cross2(p1, q1, p2, q2))

        if not any(intersect):
            return (i, j)
        else:
            dists[j] = float('Inf')


def random_map_coloring(n_points, k):
    x = np.random.uniform(size=n_points)
    y = np.random.uniform(size=n_points)

    coordinates = [(i, j) for i, j in zip(x, y)]
    connected = set()

    failed = set()
    while True:
        p = np.random.randint(low=0, high=n_points)
        if p in failed:
            continue

        connection = _argmin_connection(p, coordinates, connected)

        if connection is None:
            failed.add(p)
        else:
            connected.add(connection)

        if len(failed) == n_points:
            break

    X = coordinates
    D = [{d for d in range(k)} for v in range(n_points)]
    C = {}

    for p, q in connected:
        C[(coordinates[p], coordinates[q])] = lambda col1, col2: col1 != col2

    return {'X': X, 'D': D, 'C': C}
