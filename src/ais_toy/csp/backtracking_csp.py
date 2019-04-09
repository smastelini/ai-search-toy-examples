from csp_problem import CSPProblem


class BacktrackingCSP(CSPProblem):
    def __init__(self, X, D, C):
        super().__init__(self, X, D, C)

    def select_unassigned_var(self):
        """ Select one among the variables which were not yet assigned and
        returns it.

        Depends on a chosen heuristic. """
        pass

    def order_domain_values(self, var, assignment):
        """ Determines the order in which the possible domain's values are
        going to be evaluated.

        Also depends on a heuristic"""
        pass

    def inference(self, var, value):
        """ Used to impose some kind of consistency check."""
        pass
