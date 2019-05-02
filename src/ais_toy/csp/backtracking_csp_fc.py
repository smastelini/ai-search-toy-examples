from ais_toy.csp import BacktrackingCSP
from ais_toy.csp import forward_checking


class BacktrackingCSPFowardChecking(BacktrackingCSP):
    def __init__(self, X, D, C):
        super().__init__(X, D, C)

    def inference(self, var, value):
        """ Uses Forward Checking to impose local arc consistency. """
        checked, removed = forward_checking(var, value, self)

        return ({}, removed) if checked else (None, removed)
