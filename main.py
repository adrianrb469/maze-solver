from maze import Maze


def main():
    maze = Maze(6, 6)
    maze.visualize()
    maze.render_graph()
    # maze.save("txt")
    maze.solve("bfs")
    maze.solve("dfs")
    maze.solve("dls")
    maze.draw_solution()


if __name__ == "__main__":
    main()
