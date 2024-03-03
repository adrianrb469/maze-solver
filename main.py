from maze import Maze


def main():
    maze = Maze(3, 3)
    maze.visualize()
    maze.render_graph()
    maze.save("txt")
    maze.solve()
    maze.draw_solution()


if __name__ == "__main__":
    main()
