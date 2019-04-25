from ais_toy.csp import BacktrackingCSP
from ais_toy.csp import backtracking_search
from ais_toy.csp import forward_checking


class BacktrackingCSPFowardChecking(BacktrackingCSP):
    def __init__(self, X, D, C):
        super().__init__(X, D, C)

    def inference(self, var, value):
        """ Uses Forward Checking to impose local arc consistency. """
        checked, removed = forward_checking(var, value, self)
        inferences = {}
        if checked:
            to_assign = []
            for var in self._unassigned_variables:
                if len(self._unassigned_variables[var].domain()) == 1:
                    to_assign.append(var)
            for var in to_assign:
                value = self._unassigned_variables[var].domain()[0]
                self.assign_variable(
                    var, value
                )
                inferences[var] = value
        print(inferences)
        return (inferences, removed) if checked else (None, removed)

    def solve(self):
        return backtracking_search(self)
