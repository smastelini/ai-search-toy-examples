from .ac_3 import AC_3


def MAC(csp, x_i):
    neighbors = csp.unassigned_neighbors(x_i)
    arcs = [(x_i, x_j) for x_j in neighbors]
    return AC_3(csp, arcs)
