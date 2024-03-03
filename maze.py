import random
import matplotlib.pyplot as plt
from matplotlib import colors
from a_star import a_star_search
from bfs import bfs
from dfs import dfs
from dls import dls
from graph import Graph, Node
import networkx as nx

from greedy_bfs import greedy_bfs


class Cell:
    def __init__(self, x, y) -> None:
        self.x, self.y = x, y
        self.walls = [True, True, True, True]
        self.neighbours = []
        self.visited = False
        self.solution = False

    def find_neighbours(self, maze, maze_w, maze_h):
        if self.y > 0:
            self.neighbours.append(maze[self.x][self.y - 1])
        if self.x < maze_w - 1:
            self.neighbours.append(maze[self.x + 1][self.y])
        if self.x > 0:
            self.neighbours.append(maze[self.x - 1][self.y])
        if self.y < maze_h - 1:
            self.neighbours.append(maze[self.x][self.y + 1])


class Maze:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.maze = [[Cell(x, y) for y in range(height)] for x in range(width)]
        self.matrix = [[]]
        self.graph = None
        self.solution = []
        # generate maze -> conver to matrix -> construct graph out of the paths
        self.generate()
        self.matrix_form()
        self.construct_graph()

    # Uses randomized depth-first search to generate a maze (iterative implementation)
    def generate(self) -> None:
        # Find neighbours for each cell
        for x in range(self.width):
            for y in range(self.height):
                self.maze[x][y].find_neighbours(self.maze, self.width, self.height)

        stack = []

        current = self.maze[0][0]
        current.visited = True
        stack.append(current)

        while stack:
            current = stack[-1]

            unvisited_neighbours = [
                neighbour for neighbour in current.neighbours if not neighbour.visited
            ]

            if unvisited_neighbours:
                random_neighbour = random.choice(unvisited_neighbours)
                # remove wall between current and random neighbour
                if random_neighbour.x == current.x:
                    if random_neighbour.y > current.y:
                        current.walls[3] = False
                        random_neighbour.walls[0] = False
                    else:
                        current.walls[0] = False
                        random_neighbour.walls[3] = False
                elif random_neighbour.y == current.y:
                    if random_neighbour.x > current.x:
                        current.walls[1] = False
                        random_neighbour.walls[2] = False
                    else:
                        current.walls[2] = False
                        random_neighbour.walls[1] = False
                random_neighbour.visited = True
                stack.append(random_neighbour)
            else:
                stack.pop()

    def matrix_form(self):
        self.matrix = [
            [1 for _ in range(2 * self.width + 1)] for _ in range(2 * self.height + 1)
        ]

        for x in range(self.width):
            for y in range(self.height):
                self.matrix[2 * y + 1][2 * x + 1] = 0

                if not self.maze[x][y].walls[1]:
                    self.matrix[2 * y + 1][2 * x + 2] = 0

                if not self.maze[x][y].walls[3]:
                    self.matrix[2 * y + 2][2 * x + 1] = 0

        # pick entrance and exit randomly
        is_wall = True

        while is_wall:
            start_x, start_y = random.choice(range(self.width)), 0
            end_x, end_y = random.choice(range(self.width)), self.height - 1
            if (
                self.matrix[2 * start_y + 1][2 * start_x + 1] == 0
                and self.matrix[2 * end_y + 1][2 * end_x + 1] == 0
            ):
                is_wall = False
                self.matrix[2 * start_y + 1][2 * start_x + 1] = 2
                self.matrix[2 * end_y + 1][2 * end_x + 1] = 3

    def visualize(self):
        plt.figure(figsize=(10, 5))
        cmap = colors.ListedColormap(["white", "black", "red", "green"])

        plt.imshow(self.matrix, cmap=cmap)

        plt.axis("off")
        # Save the plot as a PNG file
        plt.savefig("maze.png")
        plt.close()

    def save(self, format="txt"):
        if format == "txt":
            # create a txt file
            with open("maze.txt", "w") as f:
                for row in self.matrix:
                    f.write("".join(str(cell) for cell in row) + "\n")
        elif format == "csv":
            # create a csv file
            with open("maze.csv", "w") as f:
                for row in self.matrix:
                    f.write(",".join(str(cell) for cell in row) + "\n")
        elif format == "python":
            # create a python file
            with open("maze.py", "w") as f:
                f.write("maze = " + str(self.matrix))

    def construct_graph(self):
        graph = Graph()

        height = len(self.matrix)
        width = len(self.matrix[0]) if height else 0

        for x in range(width):
            for y in range(height):
                if self.matrix[y][x] != 1:  # we only care about path cells
                    node = Node((x, y))
                    graph.add_node(node)

                    if self.matrix[y][x] == 2:
                        node.start = True
                        graph.start = node

                    if self.matrix[y][x] == 3:
                        node.solution = True
                        graph.end = node

        for x in range(width):
            for y in range(height):
                if self.matrix[y][x] != 1:
                    if y > 0 and self.matrix[y - 1][x] != 1:
                        graph.nodes[(x, y)].add_edge(graph.nodes[(x, y - 1)])
                    if y < height - 1 and self.matrix[y + 1][x] != 1:
                        graph.nodes[(x, y)].add_edge(graph.nodes[(x, y + 1)])
                    if x > 0 and self.matrix[y][x - 1] != 1:
                        graph.nodes[(x, y)].add_edge(graph.nodes[(x - 1, y)])
                    if x < width - 1 and self.matrix[y][x + 1] != 1:
                        graph.nodes[(x, y)].add_edge(graph.nodes[(x + 1, y)])

        self.graph = graph

    def render_graph(self):
        G = nx.Graph()

        pos = {(x, y): (x, -y) for x, y in self.graph.nodes.keys()}

        for node in self.graph.nodes.values():
            G.add_node(node.value)
            if node.solution:
                nx.set_node_attributes(G, {node.value: "green"}, "color")
            elif node.start:
                nx.set_node_attributes(G, {node.value: "red"}, "color")
            else:
                nx.set_node_attributes(G, {node.value: "lightblue"}, "color")

        for node in self.graph.nodes.values():
            for neighbour in node.adjacent:
                G.add_edge(node.value, neighbour.value)
        plt.figure(figsize=(10, 5))
        colors = nx.get_node_attributes(G, "color").values()
        nx.draw(G, pos=pos, with_labels=True, node_color=colors, node_size=600)
        plt.savefig("maze_graph.png")
        plt.close()

    def solve(self):
        def print_solution(algorithm, path, n):
            if len(path) > 0:
                print(f"---{algorithm}---")
                print(f"Solution found: {path} in {n} steps\n")
                # print("solution found")
                self.solution = path
            else:
                print("No solution found.")

        path, n = bfs(self.graph, self.graph.start, self.graph.end)

        # this is only for the final visualization, i draw the solution on the matrix
        for node in path:
            self.graph.nodes[node].solution = True

        print_solution("BFS", path, n)

        path, n = dfs(self.graph, self.graph.start, self.graph.end)

        print_solution("DFS", path, n)

        path, n = dls(self.graph, self.graph.start, self.graph.end, 100)

        print_solution("DLS", path, n)

        path, n = greedy_bfs(self.graph, self.graph.start, self.graph.end)

        print_solution("Greedy BFS Euclidean Heuristic", path, n)

        path, n = greedy_bfs(self.graph, self.graph.start, self.graph.end, "manhattan")

        print_solution("Greedy BFS Manhattan Heuristic", path, n)

        path, n = a_star_search(self.graph, self.graph.start, self.graph.end)

        print_solution("A* Euclidean Heuristic", path, n)

        path, n = a_star_search(
            self.graph, self.graph.start, self.graph.end, "manhattan"
        )

        print_solution("A* Manhattan Heuristic", path, n)

    def draw_solution(self):
        if not self.solution:
            print("Bro, you need to solve the maze first.")
            return
        # the list of tuples (x, y) representing the solution path, which we got from the solve method

        self.solution = self.solution[1:]  # remove the start node from the solution
        self.solution = self.solution[:-1]  # remove the end node from the solution

        for coord in self.solution:
            self.matrix[coord[1]][coord[0]] = 4

        plt.figure(figsize=(10, 5))
        cmap = colors.ListedColormap(["white", "black", "red", "green", "blue"])

        plt.imshow(self.matrix, cmap=cmap)

        # hide the axis
        plt.axis("off")

        # Save the plot as a PNG file
        plt.savefig("maze_solution.png")
