from abc import ABC, abstractmethod


class CSPProblem(ABC):
    class Variable:
        def __init__(self, var, to_string=str):
            self.var = var
            self._to_string = to_string

        def to_string(self):
            return self._to_string(self.var)

    def __init__(self, X, D, C):
        pass

    @abstractmethod
    def is_complete(self, assignment):
        pass

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
