from maze import Maze


def main():
    maze = Maze(4, 4)
    maze.visualize()
    maze.save("txt")
    maze.solve("bfs")
    maze.solve("dfs")


if __name__ == "__main__":
    main()
