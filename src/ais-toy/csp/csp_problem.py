from abc import ABC, abstractmethod


class CSPProblem(ABC):
    class Variable:
        def __init__(self, name, domain):
            self.value = None
            self.name = name
            if not isinstance(domain, set):
                self._domain = set(domain)
            else:
                self._domain = domain

        def domain(self):
            return self._domain.tolist()

        def rem_from_domain(self, x):
            if x in self._domain:
                self._domain.remove(x)

    def __init__(self, X, D, C):
        if len(X) != len(D):
            raise ValueError('The lengths of X and D must be the same.')

        self._unassigned_variables = {}
        self._assigned_variables = {}
        for i in range(len(X)):
            self._unassigned_variables[X[i]] = self.Variable(X[i], D[i])

        # TODO to deal with the constraints

    def _build_constraint_graph(self):
        pass

    @abstractmethod
    def is_complete(self, assignment):
        return len(self._unassigned_variables) == 0

    @abstractmethod
    def select_unassigned_var(self):
        """ Select one among the variables which were not yet assigned and
        returns it.

        Depends on a chosen heuristic. """
        pass

    @abstractmethod
    def order_domain_values(self, var, assignment):
        """ Determines the order in which the possible domain's values are
        going to be evaluated.

        Also depends on a heuristic"""
        pass

    def is_consistent(self, value, assignment):
        pass

    @abstractmethod
    def inference(self, var, value):
        """ Used to impose some kind of consistency check."""
        pass

    def get_all_arcs(self):
        """ Get all the current arcs in the restriction graph. """
        pass

    def constraint_checks(x_i, x_j, x, j):
        pass

    def neighbours_except(self, x_i, x_j):
        pass

    def get_complete_assignement(self):
        pass

    def is_solution(self, candidate):
        pass

    def argmin_conflicts(self, var, candidate):
        pass

    def unassigned_neighbours(self, x_i, x_j):
        pass
