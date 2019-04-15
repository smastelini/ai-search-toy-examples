class Node:
    def __init__(self, state):
        self.state = state
        self._edges = []

    def add_edge(self, node, cost=1):
        self._edges.append((node, cost))
