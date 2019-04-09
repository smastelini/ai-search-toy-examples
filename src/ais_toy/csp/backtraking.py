def backtracking_search(csp):
    return _backtrack({}, csp)


def _backtrack(assignment, csp):
    if csp.is_complete(assignment):
        return assignment

    var = csp.select_unassigned_var()
    for value in csp.order_domain_values(var, assignment):
        if csp.is_consistent(var, value, assignment):
            assignment[var.name] = value
            csp.assign_variable(var.name, value)
            inferences = csp.inference(var, value)
            if inferences is not None:
                assignment.update(inferences)
                result = _backtrack(assignment, csp)
                if result is not None:
                    return result
        if var.name in assignment:
            csp.unassign_variable(var.name)
            del assignment[var.name]
        if inferences is not None:
            for inference in inferences:
                csp.unassign_variable(inference)
                assignment.pop(inference, None)
    return None
