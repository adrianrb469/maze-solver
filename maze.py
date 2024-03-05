import random
import time
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
    def __init__(self, width: int = 0, height: int = 0, filename: str = None) -> None:
        self.width = width
        self.height = height
        self.maze = [[Cell(x, y) for y in range(height)] for x in range(width)]
        self.matrix = [[]]
        self.graph = None
        self.solution = []

        if filename:
            self.load_from_txt(filename)  # loads the matrix directly from a txt file
        else:
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
            [0 for _ in range(2 * self.width + 1)] for _ in range(2 * self.height + 1)
        ]

        for x in range(self.width):
            for y in range(self.height):
                self.matrix[2 * y + 1][2 * x + 1] = 1

                if not self.maze[x][y].walls[1]:
                    self.matrix[2 * y + 1][2 * x + 2] = 1

                if not self.maze[x][y].walls[3]:
                    self.matrix[2 * y + 2][2 * x + 1] = 1

        # pick entrance and exit randomly
        is_wall = True

        while is_wall:
            start_x, start_y = random.choice(range(self.width)), 0
            end_x, end_y = random.choice(range(self.width)), self.height - 1
            if (
                self.matrix[2 * start_y + 1][2 * start_x + 1] == 1
                and self.matrix[2 * end_y + 1][2 * end_x + 1] == 1
            ):
                is_wall = False
                self.matrix[2 * start_y + 1][2 * start_x + 1] = 2
                self.matrix[2 * end_y + 1][2 * end_x + 1] = 3

    def load_from_txt(self, filename):
        with open(filename, "r") as f:
            self.matrix = [
                [int(cell) for cell in line.strip()] for line in f.readlines()
            ]
        self.width = len(self.matrix[0]) // 2
        self.height = len(self.matrix) // 2
        self.construct_graph()

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
                if self.matrix[y][x] != 0:  # we only care about path cells
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
                if self.matrix[y][x] != 0:
                    if y > 0 and self.matrix[y - 1][x] != 0:
                        graph.nodes[(x, y)].add_edge(graph.nodes[(x, y - 1)])
                    if y < height - 1 and self.matrix[y + 1][x] != 0:
                        graph.nodes[(x, y)].add_edge(graph.nodes[(x, y + 1)])
                    if x > 0 and self.matrix[y][x - 1] != 0:
                        graph.nodes[(x, y)].add_edge(graph.nodes[(x - 1, y)])
                    if x < width - 1 and self.matrix[y][x + 1] != 0:
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
                nx.set_node_attributes(G, {node.value: "black"}, "color")

        for node in self.graph.nodes.values():
            for neighbour in node.adjacent:
                G.add_edge(node.value, neighbour.value)

        plt.figure(figsize=(20, 20))
        colors = nx.get_node_attributes(G, "color").values()
        nx.draw(G, pos=pos, node_color=colors, node_size=100)
        plt.savefig("maze_graph.png")
        plt.close()

    def solve(self):
        solutions = []

        def print_solution(algorithm, path, n, execution_time):
            if len(path) > 0:
                print(f"---{algorithm}---")
                print(f"Solution found: in {len(path)} steps")
                print(f"Execution time: {execution_time} seconds")
                self.solution = path
                solutions.append((algorithm, len(path), execution_time))
            else:
                print("No solution found.")

        algorithms = [
            ("BFS", bfs),
            ("DFS", dfs),
            ("DLS", dls, 800),
            ("Greedy BFS Euclidean Heuristic", greedy_bfs),
            (
                "Greedy BFS Manhattan Heuristic",
                lambda graph, start, end: greedy_bfs(graph, start, end, "manhattan"),
            ),
            ("A* Euclidean Heuristic", a_star_search),
            (
                "A* Manhattan Heuristic",
                lambda graph, start, end: a_star_search(graph, start, end, "manhattan"),
            ),
        ]

        for algorithm_name, algorithm, *args in algorithms:
            start_time = time.time()
            path, n = algorithm(self.graph, self.graph.start, self.graph.end, *args)
            end_time = time.time()

            for node in path:
                self.graph.nodes[node].solution = True

            self.solution = path
            solutions.append((algorithm_name, len(path), end_time - start_time))
            # print_solution(algorithm_name, path, n, end_time - start_time)

        return solutions

    def draw_solution(self, filename):
        if not self.solution:
            print("Bro, you need to solve the maze first.")
            return
        # the list of tuples (x, y) representing the solution path, which we got from the solve method

        self.solution = self.solution[1:]  # remove the start node from the solution
        self.solution = self.solution[:-1]  # remove the end node from the solution

        for coord in self.solution:
            self.matrix[coord[1]][coord[0]] = 4

        plt.figure(figsize=(10, 5))
        cmap = colors.ListedColormap(["black", "white", "red", "green", "blue"])

        plt.imshow(self.matrix, cmap=cmap)

        # hide the axis
        plt.axis("off")

        # Save the plot as a PNG file
        plt.savefig(filename + ".png")
