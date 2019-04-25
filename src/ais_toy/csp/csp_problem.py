import numpy as np
from abc import ABC, abstractmethod
from ais_toy.struct import Incognita, Node, Graph


class CSPProblem(ABC):
    def __init__(self, X, D, C):
        if len(X) != len(D):
            raise ValueError('The lengths of X and D must be the same.')

        self._unassigned_variables = {}
        self._assigned_variables = {}
        for i in range(len(X)):
            self._unassigned_variables[X[i]] = Incognita(X[i], D[i])

        self._constraints = C
        self._constraint_graph = self._build_constraint_graph()
        self._arcs = [k for k in self._constraints.keys()]

    def _build_constraint_graph(self):
        nodes = {}

        for p in self._unassigned_variables.keys():
            nodes[p] = Node(p)

        for p, q in self._constraints.keys():
            nodes[p].add_edge(nodes[q])
            nodes[q].add_edge(nodes[p])

        g = Graph()
        g.add_multiple_nodes([n for n in nodes.values()])

        return g

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

    @abstractmethod
    def inference(self, var, value):
        """ Used to impose some kind of consistency check."""
        pass

    @abstractmethod
    def solve(self, *args, **kwargs):
        """ Method that effectively solves the CSP problem. """
        pass

    def is_complete(self, assignment):
        return len(self._unassigned_variables) == 0

    def assign_variable(self, var, value):
        if isinstance(var, Incognita):
            var = var.name
        if var in self._unassigned_variables:
            self._assigned_variables[var] = self._unassigned_variables.pop(
                var
            )
        self._assigned_variables[var].assign(value)

    def unassign_variable(self, var):
        if isinstance(var, Incognita):
            var = var.name
        self._assigned_variables[var].unassign()
        self._unassigned_variables[var] = self._assigned_variables.pop(var)

    def is_consistent(self, var, value, assignment):
        ngbs = [p[0].state for p in self._constraint_graph.neighbors(var.name)]
        check = []
        for n in ngbs:
            if n in assignment:
                check.append(
                    self.constraint_checks(var.name, n, value, assignment[n])
                )

        return np.all(check)

    def get_all_arcs(self):
        """ Get all the current arcs in the restriction graph. """
        return self._arcs

    def constraint_checks(self, x_i, x_j, x, y):
        return self._constraints[(x_i, x_j)](x, y) \
            if (x_i, x_j) in self._constraints else \
            self._constraints[(x_j, x_i)](y, x)

    def neighbors_except(self, x_i, x_j):
        neighbors = self._constraint_graph.neighbors(x_i)
        selected = [p[0].state for p in neighbors if p[0].state != x_j and
                    p[0].state in self._unassigned_variables]
        # TODO verificar se sao apenas as unassigned
        return selected

    def is_solution(self, candidate):
        for incg in candidate:
            ngbr = [
                n[0].state for n in self._constraint_graph.neighbors(incg)
            ]
            for n in ngbr:
                if not self.constraint_checks(incg, n, candidate[incg],
                                              candidate[n]):
                    return False

        return True

    def unassigned_neighbors(self, x_i):
        neighbors = [n[0].state for n in self._constraint_graph.neighbors(x_i)
                     if n[0].state in self._unassigned_variables]
        return neighbors

    def domain(self, var_id):
        if var_id in self._unassigned_variables:
            return self._unassigned_variables[var_id].domain()
        else:
            return [self._assigned_variables[var_id].value]

    def rem_from_domain(self, var_id, val):
        return self._unassigned_variables[var_id].rem_from_domain(val)

    def restore_modified_domains(self, removed):
        for var, value in removed:
            self._unassigned_variables[var].expand_domain(value)
