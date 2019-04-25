def forward_checking(var, value, csp):
    removed = []
    ngbrs = csp.unassigned_neighbors(var.name)

    for n in ngbrs:
        # Pode dar problema por alterar o dominio on the fly
        for v in csp._unassigned_variables[n].domain():
            if not csp.constraint_checks(var.name, n, value, v):
                removed.append((n, v))
                csp.rem_from_domain(n, v)
        if len(csp._unassigned_variables[n].domain()) == 0:
            return False, removed
    return True, removed
