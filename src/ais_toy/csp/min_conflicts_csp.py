import numpy as np
from .csp_problem import CSPProblem
from .min_conflicts import min_conflicts


class MinConflictsCSP(CSPProblem):
    def __init__(self, X, D, C):
        super().__init__(X, D, C)
        self._assigned_variables = self._unassigned_variables
        self._unassigned_variables = {}

    def get_complete_assignment(self):
        """ Used by the local search methods, which deal with complete
        assignments"""
        r_assign = {}
        for val, var in self._assigned_variables.items():
            dmn = var.domain()
            d_idx = np.random.randint(
                low=0, high=len(dmn)
            )
            r_assign[val] = dmn[d_idx]
            self.assign_variable(val, dmn[d_idx])
        return r_assign

    def domain(self, var_id):
        return self._assigned_variables[var_id].domain()

    def rem_from_domain(self, var_id, val):
        return self._assigned_variables[var_id].rem_from_domain(val)

    def select_unassigned_var(self):
        confliting_vars = []
        for val, var in self._assigned_variables.items():
            ngbrs = [
                n[0].state for n in self._constraint_graph.neighbors(val)
            ]
            for n in ngbrs:
                if not self.constraint_checks(
                    val, n, var.value, self._assigned_variables[n].value
                ):
                    confliting_vars.append(val)
                    break
        sel = np.random.randint(low=0, high=len(confliting_vars))
        return self._assigned_variables[confliting_vars[sel]]

    def order_domain_values(self, var, assignment):
        raise NotImplementedError

    def inference(self, var, value):
        raise NotImplementedError

    def solve(self, max_steps):
        """ Method that effectively solves the CSP problem. """
        return min_conflicts(self, max_steps)

    def argmin_conflicts(self, var):
        conflicts = {}
        ngbrs = [
            n[0].state for n in self._constraint_graph.neighbors(var.name)
        ]
        for v in var.domain():
            count = 0
            for n in ngbrs:
                count += int(
                    not self.constraint_checks(
                        var.name, n, v, self._assigned_variables[n].value
                    )
                )
            conflicts[v] = count
        return min(conflicts, key=conflicts.get)
