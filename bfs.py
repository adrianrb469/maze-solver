from graph import Graph, Node
from timer import timer


@timer
def bfs(graph: Graph, start: Node, end: Node) -> tuple:
    queue = [start]
    visited = {start: None}
    steps = 0

    while queue:
        steps += 1
        current = queue.pop(0)

        # we found solution, just walk back to start
        if current == end:
            path = []
            while current:
                path.append(current.value)
                current = visited[current]
            return path[::-1], steps

        for neighbour in current.get_neighbours():
            if neighbour not in visited:
                queue.append(neighbour)
                visited[neighbour] = current

    return [], steps


export = bfs
