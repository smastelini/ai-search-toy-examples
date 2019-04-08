def min_conflicts(csp, max_steps):
    current = csp.get_complete_assignment()
    for i in range(max_steps):
        if csp.is_solution(current):
            return current
        var = csp.select_unassigned_var()
        value = csp.argmin_conflicts(var, current)
        current[var.name] = value
    return None
