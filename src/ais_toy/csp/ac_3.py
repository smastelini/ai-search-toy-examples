def AC_3(csp, queue=None):
    if queue is None:
        queue = csp.get_all_arcs()

    while len(queue) > 0:
        x_i, x_j = queue.pop(0)
        if _revise(csp, x_i, x_j):
            if len(x_i.domain()) == 0:
                return False
            for x_k in csp.neighbors_except(x_i, x_j):
                queue.append((x_k, x_i))
    return True


def _revise(csp, x_i, x_j):
    revised = False
    for x in x_i.domain():
        satisfies = False
        for y in x_j.domain():
            satisfies = csp.constraint_checks(x_i, x_j, x, y)
            if satisfies:
                break
        if not satisfies:
            x_i.rem_from_domain(x)
            revised = True
    return revised
