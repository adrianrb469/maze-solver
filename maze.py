import random
import matplotlib.pyplot as plt
from matplotlib import colors
from bfs import bfs
from dfs import dfs
from graph import Graph, Node
import networkx as nx


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
        self.generate()
        self.matrix_form()

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
        print("plot ", self.matrix)
        cmap = colors.ListedColormap(["white", "black", "red", "green"])

        plt.imshow(self.matrix, cmap=cmap)

        # Add numbers to the cells
        for x in range(2 * self.width + 1):
            for y in range(2 * self.height + 1):
                plt.text(
                    y, x, str(self.matrix[x][y]), ha="center", va="center", color="blue"
                )

        # Save the plot as a PNG file
        plt.savefig("maze.png")

        plt.show()

    # txt, csv, or python matrix
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

    def solve(self, method="bfs"):
        print("graph ", self.matrix)
        G = nx.Graph()
        graph = Graph()

        height = len(self.matrix)
        width = len(self.matrix[0]) if height else 0

        start = None
        end = None

        # Create a node for each path cell and add it to the graph
        for x in range(width):
            for y in range(height):
                if self.matrix[y][x] != 1:  # Only add the node if it's not a wall
                    G.add_node((x, y))
                    node = Node((x, y))
                    graph.add_node(node)

                    # keep a reference to the start node
                    if self.matrix[y][x] == 2:
                        start = node

                    # mark the end node as a solution
                    if self.matrix[y][x] == 3:
                        node.solution = True
                        end = node

        # Add edges between neighboring path cells
        for x in range(width):
            for y in range(height):
                if self.matrix[y][x] != 1:  # Only consider the node if it's not a wall
                    if y > 0 and self.matrix[y - 1][x] != 1:
                        G.add_edge((x, y), (x, y - 1))
                        graph.nodes[(x, y)].add_edge(graph.nodes[(x, y - 1)])
                    if y < height - 1 and self.matrix[y + 1][x] != 1:
                        G.add_edge((x, y), (x, y + 1))
                        graph.nodes[(x, y)].add_edge(graph.nodes[(x, y + 1)])
                    if x > 0 and self.matrix[y][x - 1] != 1:
                        G.add_edge((x, y), (x - 1, y))
                        graph.nodes[(x, y)].add_edge(graph.nodes[(x - 1, y)])
                    if x < width - 1 and self.matrix[y][x + 1] != 1:
                        G.add_edge((x, y), (x + 1, y))
                        graph.nodes[(x, y)].add_edge(graph.nodes[(x + 1, y)])

        pos = {(x, y): (x, -y) for x, y in G.nodes()}
        nx.draw(G, pos=pos, with_labels=True, node_color="skyblue", node_size=600)
        plt.savefig("maze_graph.png")
        plt.show()

        if method == "bfs":
            path = bfs(graph, start, end)
            if len(path) > 0:
                print("Solution found: ", path)
            else:
                print("Sowwy, no solution found :(")
        if method == "dfs":
            path = dfs(graph, start, end)
            if len(path) > 0:
                print("Solution found: ", path)
            else:
                print("Sowwy, no solution found :(")
