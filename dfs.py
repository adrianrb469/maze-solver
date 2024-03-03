from graph import Graph, Node


def dfs(graph: Graph, start: Node, end: Node) -> list:
    stack = [start]
    visited = {start: None}

    while stack:
        current = stack.pop()

        # we found solution, just walk back to start
        if current == end:
            path = []
            while current:
                path.append(current.value)
                current = visited[current]
            return path[::-1]

        for neighbour in current.get_neighbours():
            if neighbour not in visited:
                stack.append(neighbour)
                visited[neighbour] = current
    return []


export = dfs
