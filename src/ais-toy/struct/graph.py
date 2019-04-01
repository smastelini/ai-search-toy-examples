class DirGraph:
    def __init__(self, nodes=[]):
        self._nodes = nodes

    def add_node(self, node):
        self._nodes.append(node)

    def add_multiple_nodes(self, nodes):
        self._nodes.extend(nodes)
