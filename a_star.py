import heapq
from timer import timer

from graph import Graph, Node


def heuristic(node, end, type="euclidean"):
    x1, y1 = node
    x2, y2 = end

    if type == "euclidean":
        distance = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
    else:
        distance = abs(x1 - x2) + abs(y1 - y2)
    return distance


@timer
def a_star_search(
    graph: Graph, start: Node, end: Node, heuristic_t="euclidean"
) -> tuple:
    queue = [
        (0, start.value, start)
    ]  # The queue stores tuples of (cost + heuristic, value, node)
    costs = {start: 0}
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
            new_cost = costs[current] + 1
            if neighbour not in costs or new_cost < costs[neighbour]:
                costs[neighbour] = new_cost
                priority = new_cost + heuristic(neighbour.value, end.value, heuristic_t)
                heapq.heappush(queue, (priority, neighbour.value, neighbour))
                visited[neighbour] = current

    return [], steps


export = a_star_search
