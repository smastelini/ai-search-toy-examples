from ais_toy.csp import BacktrackingCSP
from ais_toy.csp import MAC


class BacktrackingCSPMAC(BacktrackingCSP):
    def __init__(self, X, D, C):
        super().__init__(X, D, C)

    def inference(self, var, value):
        """ Uses MAC to impose arc consistency. """
        checked, removed = MAC(self, var.name)

        return ({}, removed) if checked else (None, removed)
