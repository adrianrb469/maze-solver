from graph import Graph, Node


def bfs(graph: Graph, start: Node, end: Node) -> list:
    queue = [start]
    visited = {start: None}

    while queue:
        current = queue.pop(0)

        # we found solution, just walk back to start
        if current == end:
            path = []
            while current:
                path.append(current.value)
                current = visited[current]
            return path[::-1]

        for neighbour in current.get_neighbours():
            if neighbour not in visited:
                queue.append(neighbour)
                visited[neighbour] = current
    return []


export = bfs
