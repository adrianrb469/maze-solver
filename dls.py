from graph import Graph, Node
from timer import timer


@timer
def dls(graph: Graph, start: Node, end: Node, limit: int) -> list:
    return dls_rec(graph, start, end, limit, {start: None}, 0)


def dls_rec(
    graph: Graph, current: Node, end: Node, limit: int, visited: dict, steps: int
) -> tuple:
    if current == end:
        path = []
        while current:
            path.append(current.value)
            current = visited[current]
        return path[::-1], steps

    if limit <= 0:
        return [], steps

    for neighbour in current.get_neighbours():
        if neighbour not in visited:
            visited[neighbour] = current
            path, steps = dls_rec(graph, neighbour, end, limit - 1, visited, steps + 1)
            if path:
                return path, steps

    return [], steps


export = dls
