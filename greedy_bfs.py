import heapq

from graph import Graph, Node
from timer import timer


def heuristic(node, end, type="euclidean"):
    # we can do this because each node has a value (x, y) (point in the maze)
    x1, y1 = node
    x2, y2 = end

    # euclidean distance
    if type == "euclidean":
        distance = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
    else:
        distance = abs(x1 - x2) + abs(y1 - y2)
    return distance


@timer
def greedy_bfs(graph: Graph, start: Node, end: Node, heuristic_t="euclidean") -> tuple:
    queue = [
        (0, start.value, start)
    ]  # The queue stores tuples of (heuristic, value, node)
    visited = {start: None}
    steps = 0

    while queue:
        _, _, current = heapq.heappop(queue)
        steps += 1

        if current == end:
            path = []
            while current:
                path.append(current.value)
                current = visited[current]
            return path[::-1], steps

        for neighbour in current.get_neighbours():
            if neighbour not in visited:
                heapq.heappush(
                    queue,
                    (
                        heuristic(neighbour.value, end.value, heuristic_t),
                        neighbour.value,
                        neighbour,
                    ),
                )
                visited[neighbour] = current

    return [], steps
