from .ac_3 import AC_3


def MAC(csp, x_i):
    neighbours = csp.unassigned_neighbours(x_i)
    arcs = [(x_i, x_j) for x_j in neighbours]
    return AC_3(csp, arcs)
