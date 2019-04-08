import numpy as np
from abc import ABC, abstractmethod
from ais_toy.struct import Variable, Node, Graph


class CSPProblem(ABC):
    def __init__(self, X, D, C):
        if len(X) != len(D):
            raise ValueError('The lengths of X and D must be the same.')

        self._unassigned_variables = {}
        self._assigned_variables = {}
        for i in range(len(X)):
            self._unassigned_variables[X[i]] = Variable(X[i], D[i])

        self._constraints = C
        self._constraint_graph = self._build_constraint_graph()
        self._arcs = [k for k in self._constraints.keys()]

    def _build_constraint_graph(self):
        nodes = {}

        for p, q in self._constraints.keys():
            if p not in nodes:
                nodes[p] = Node(p)

            if q not in nodes:
                nodes[q] = Node(q)

        for p, q in self._constraints.keys():
            nodes[p].add_edge(nodes[q])

        g = Graph()
        g.add_multiple_nodes([n for n in nodes.values()])

        return g

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

    def is_consistent(self, var, value, assignment):
        ngbs = [p.state for p in self._constraint_graph.neighbors(var.name)]
        check = []
        for n in ngbs:
            if n in assignment:
                check.append(
                    self._constraints[(var.name, n)](value, assignment[n])
                    if (var.name, n) in self._constraints else
                    self._constraints[(n, var.name)](assignment[n], value)
                )

        return np.all(check)

    @abstractmethod
    def inference(self, var, value):
        """ Used to impose some kind of consistency check."""
        pass

    def get_all_arcs(self):
        """ Get all the current arcs in the restriction graph. """
        return self._arcs

    def constraint_checks(self, x_i, x_j, x, y):
        return self._constraints[(x_i, x_j)](x, y)

    def neighbours_except(self, x_i, x_j):
        neighbours = self._constraint_graph.neighbors(x_i)
        selected = [p.state for p in neighbours if p.state != x_j]
        return selected

    def get_complete_assignement(self):
        r_assign = {}
        for val, var in self._unassigned_variables.items():
            dmn = var.domain()
            d_idx = np.random.randint(
                low=0, high=len(dmn)
            )
            r_assign[val] = dmn[d_idx]
        return r_assign

    def is_solution(self, candidate):
        pass

    def argmin_conflicts(self, var, candidate):
        pass

    def unassigned_neighbours(self, x_i):
        neighbours = self._constraint_graph.neighbors(x_i)
        selected = [p.state for p in neighbours if p.state in
                    self._unassigned_variables]
        return selected
