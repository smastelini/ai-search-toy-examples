class Node:
    def __init__(self, state):
        self.state = state
        self._edges = []

    def add_edge(self, state, cost=1):
        self._edges.append((state, cost))
