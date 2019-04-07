class Node:
    def __init__(self, state, directed=False):
        self.state = state
        self._edges_out = []
        self._directed = directed

        if not self._directed:
            self._edges_in = []

    def add_edge(self, node, cost=1):
        self._edges_out.append((node, cost))
        if not self._directed:
            node._edges_in.append((self, cost))
