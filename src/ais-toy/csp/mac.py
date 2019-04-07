from .ac_3 import AC_3


def MAC(csp, x_i):
    neighbours = csp.unassigned_neighbours(x_i)
    return AC_3(csp, neighbours)
