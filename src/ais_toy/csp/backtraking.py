def backtracking_search(csp):
    return _backtrack({}, csp)


def _backtrack(assignment, csp):
    if csp.is_complete(assignment):
        return assignment

    var = csp.select_unassigned_var()
    for value in csp.order_domain_values(var):
        inferences = None
        removed = []
        if csp.is_consistent(var, value, assignment):
            csp.assign_variable(var, value)
            assignment[var.name] = value
            inferences, removed = csp.inference(var, value)
            if inferences is not None:
                assignment.update(inferences)
                result = _backtrack(assignment, csp)
                if result is not None:
                    return result
        if var.name in assignment:
            csp.unassign_variable(var)
            assignment.pop(var.name, None)
        if inferences is not None:
            for inference in inferences:
                csp.unassign_variable(inference)
                assignment.pop(inference, None)
        csp.restore_modified_domains(removed)
    return None
