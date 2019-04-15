def minimum_remaining_values(csp):
    """ The MRV heuristic

        Parameters
        ----------
            csp: a CSPProblem object

        Returns
        -------
            min, counts: var_id, dict
                The id of the variable with the smallest allowed
                domain, and the domain sizes for each unassigned variables,
                respectively.
    """
    counts = {}

    for id, var in csp._unassigned_variables.items():
        counts[id] = len(var.domain())

    return min(counts, key=counts.get), counts


def degree_heuristic(csp):
    """ The degree heuristic

        Parameters
        ----------
            csp: a CSPProblem object

        Returns
        -------
            max, counts: var_id, dict
                The id of the variable which is involved in the largest number
                of constraints(among all the unassigned variables), and the
                amount of constraints which each variable is envolved with,
                respectively.
    """
    counts = {}

    for id in csp._unassigned_variables:
        counts[id] = len(csp._constraint_graph.neighbors(id))

    return max(counts, key=counts.get), counts


def least_constraining_value(csp, var_id):
    var = csp._unassigned_variables[var_id]
    neighbors_ids = [p for p in
                     csp._constraint_graph.neighbors(var.name)]
    fail_check = {}
    for val in var.domain():
        fail_check[val] = 0
        for n in neighbors_ids:
            if n not in csp._unassigned_variables:
                continue
            for v in csp._unassigned_variables[n].domain():
                aux = csp._constraints[(var_id, n)](val, v) if (var_id, n) in \
                    csp._constraints[(var_id, n)] else \
                    csp._constraints[(n, var_id)](v, val)
                fail_check[val] += 1 if not aux else 0
    return sorted(fail_check, key=fail_check.get)
