from graph import Graph, Node
from timer import timer


@timer
def dfs(graph: Graph, start: Node, end: Node) -> tuple:
    stack = [start]
    visited = {start: None}
    steps = 0

    while stack:
        current = stack.pop()
        steps += 1

        # we found solution, just walk back to start
        if current == end:
            path = []
            while current:
                path.append(current.value)
                current = visited[current]
            return path[::-1], steps

        for neighbour in current.get_neighbours():
            if neighbour not in visited:
                stack.append(neighbour)
                visited[neighbour] = current
    return [], steps


export = dfs
