class Node:
    def __init__(self, value) -> None:
        self.value = value  # (x, y) to uniquely identify the node
        self.adjacent = {}  # key: node, value: weight
        self.visited = False
        self.solution = False
        self.start = False

    def add_edge(self, node, weight=1):
        self.adjacent[node] = weight

    def get_neighbours(self):
        return self.adjacent.keys()

    def get_weight(self, node):
        return self.adjacent[node]


class Graph:
    def __init__(self):
        self.nodes = {}
        self.start = None
        self.end = None

    def add_node(self, node):
        self.nodes[node.value] = node  # key: (x, y), value: node
