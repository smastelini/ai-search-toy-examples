import numpy as np
from .csp_problem import CSPProblem
from .min_conflicts import min_conflicts
from ais_toy.struct import Incognita


class MinConflictsCSP(CSPProblem):
    def __init__(self, X, D, C):
        super().__init__(X, D, C)

    def assign_variable(self, var, value):
        if isinstance(var, Incognita):
            var = var.name
        self._unassigned_variables[var].value = value

    def get_complete_assignment(self):
        """ Used by the local search method, which deal with complete
        assignments"""
        r_assign = {}
        for val, var in self._unassigned_variables.items():
            dmn = var.domain()
            d_idx = np.random.randint(
                low=0, high=len(dmn)
            )
            r_assign[val] = dmn[d_idx]
            self.assign_variable(val, dmn[d_idx])
        return r_assign

    def is_solution(self, candidate):
        for incg in candidate:
            ngbr = self._constraint_graph.neighbors(incg)

            for n in ngbr:
                if not self.constraint_checks(incg, n, candidate[incg],
                                              candidate[n]):
                    return False

        return True

    def domain(self, var_id):
        return self._unassigned_variables[var_id].domain()

    def select_unassigned_var(self):
        confliting_vars = []
        for var in self._unassigned_variables.values():
            ngbrs = self._constraint_graph.neighbors(var.name)

            for n in ngbrs:
                if not self.constraint_checks(
                    var.name, n, var.value, self._unassigned_variables[n].value
                ):
                    confliting_vars.append(var.name)
                    break
        sel = np.random.randint(low=0, high=len(confliting_vars))
        return self._unassigned_variables[confliting_vars[sel]]

    def order_domain_values(self, var, assignment):
        raise NotImplementedError

    def inference(self, var, value):
        raise NotImplementedError

    def solve(self, max_steps):
        """ Method that effectively solves the CSP problem. """
        return min_conflicts(self, max_steps)

    def argmin_conflicts(self, var):
        conflicts = {}
        ngbrs = self._constraint_graph.neighbors(var.name)
        for v in var.domain():
            count = 0
            for n in ngbrs:
                count += int(
                    not self.constraint_checks(
                        var.name, n, v, self._unassigned_variables[n].value
                    )
                )
            conflicts[v] = count
        min_v = min(conflicts.values())
        candidates = [n for n in conflicts
                      if conflicts[n] == min_v]
        return candidates[np.random.randint(low=0, high=len(candidates))]
