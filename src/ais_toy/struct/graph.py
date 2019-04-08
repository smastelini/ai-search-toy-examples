class Graph:
    def __init__(self, nodes={}):
        self._nodes = nodes

    def add_node(self, node):
        self._nodes[node.state] = node

    def add_multiple_nodes(self, nodes):
        self._nodes.update({node.state: node for node in nodes})

    def n_nodes(self):
        return len(self._nodes)

    def neighbors(self, id):
        return self._nodes[id]._edges
