from ais_toy.csp import CSPProblem
from ais_toy.csp.heuristics import minimum_remaining_values, \
    degree_heuristic, least_constraining_value
from ais_toy.csp import backtracking_search


class BacktrackingCSP(CSPProblem):
    def __init__(self, X, D, C):
        super().__init__(X, D, C)

    def select_unassigned_var(self):
        min_, counts = minimum_remaining_values(self)
        if list(counts.values()).count(counts[min_]) > 1:
            max_, _ = degree_heuristic(self)
            return self._unassigned_variables[max_]
        else:
            return self._unassigned_variables[min_]

    def order_domain_values(self, var):
        """ Determines the order in which the possible domain's values are
        going to be evaluated.

        Use the least constraining value for this end.
        """
        return least_constraining_value(self, var.name)

    def inference(self, var, value):
        return ({}, [])

    def solve(self):
        return backtracking_search(self)
