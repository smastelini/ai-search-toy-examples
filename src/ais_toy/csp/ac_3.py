def AC_3(csp, queue=None):
    if queue is None:
        queue = csp.get_all_arcs()

    while len(queue) > 0:
        x_i, x_j = queue.pop(0)
        if _revise(csp, x_i, x_j):
            if len(csp.domain(x_i)) == 0:
                return False
            for x_k in csp.neighbors_except(x_i, x_j):
                queue.append((x_k, x_i))
    return True


def _revise(csp, x_i, x_j):
    revised = False
    for x in csp.domain(x_i):
        satisfies = False
        for y in csp.domain(x_j):
            satisfies = csp.constraint_checks(x_i, x_j, x, y)
            if satisfies:
                break
        if not satisfies:
            csp.rem_from_domain(x_i, x)
            revised = True
    return revised
