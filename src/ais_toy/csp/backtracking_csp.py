from ais_toy.csp import CSPProblem
from ais_toy.csp.heuristics import minimum_remaining_values, \
    degree_heuristic, least_constraining_value
from ais_toy.csp import AC_3
from ais_toy.csp import backtracking_search


class BacktrackingCSP(CSPProblem):
    def __init__(self, X, D, C):
        super().__init__(self, X, D, C)

    def select_unassigned_var(self):
        min_, counts = minimum_remaining_values(self)
        if list(counts.values()).count(counts[min_]) > 1:
            max_, _ = degree_heuristic(self)
            return max_
        else:
            return min_

    def order_domain_values(self, var):
        """ Determines the order in which the possible domain's values are
        going to be evaluated.

        Use the least constraining value for this end.
        """
        return least_constraining_value(self, var)

    def inference(self, var, value):
        """ Uses AC-3 to impose arc consistency. """
        checked = AC_3(self)
        return {} if checked else None

    def solve(self):
        backtracking_search(self)
