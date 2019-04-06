def backtracking_search(csp):
    return _backtrack({}, csp)


def _backtrack(assignment, csp):
    if csp.is_complete(assignment):
        return assignment

    var = csp.select_unassigned_var()
    for value in csp.order_domain_values(var, assignment):
        if csp.is_consistent(value, assignment):
            assignment[var.to_string()] = value
            inferences = csp.inference(var, value)
            if inferences is not None:
                assignment.update(inferences)
                result = _backtrack(assignment, csp)
                if result is not None:
                    return result
        if var.name in assignment:
            del assignment[var.name]
        if inferences is not None:
            for inference in inferences:
                assignment.pop(inference, None)
    return None
