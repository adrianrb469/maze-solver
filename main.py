from maze import Maze


def main():
    maze = Maze(4, 4)
    maze.generate()
    maze.visualize()
    maze.save("csv")


if __name__ == "__main__":
    main()
