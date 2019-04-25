def AC_3(csp, queue=None):
    if queue is None:
        queue = csp.get_all_arcs()

    removed = []

    while len(queue) > 0:
        x_i, x_j = queue.pop(0)
        revise, removed = _revise(csp, x_i, x_j, removed)
        if revise:
            if len(csp.domain(x_i)) == 0:
                return False, removed
            for x_k in csp.neighbors_except(x_i, x_j):
                queue.append((x_k, x_i))
    return True, removed


def _revise(csp, x_i, x_j, removed):
    revised = False
    for x in csp.domain(x_i):
        satisfies = False
        for y in csp.domain(x_j):
            satisfies = csp.constraint_checks(x_i, x_j, x, y)
            if satisfies:
                break
        if not satisfies:
            removed.append((x_i, x))
            csp.rem_from_domain(x_i, x)
            revised = True
    return revised, removed
