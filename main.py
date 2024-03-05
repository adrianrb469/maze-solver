from maze import Maze


def main():
    solutions = []

    # for i in range(5):
    #     maze = Maze(30, 30)
    #     maze.visualize()
    #     maze.render_graph()
    #     maze.save(f"maze_generated_{i}")
    #     solution = maze.solve()
    #     maze.draw_solution(f"maze_generated_{i}_solution")
    #     solutions.append(solution)

    filenames = ["maze1.txt", "maze2.txt", "maze3.txt", "maze4.txt"]
    for filename in filenames:
        maze = Maze(0, 0, filename)
        maze.visualize()
        maze.render_graph()
        solution = maze.solve()
        maze.draw_solution(f"{filename}_solution")
        solutions.append(solution)

    # Print solutions
    for i, maze_solutions in enumerate(solutions):
        print(f"Maze {i+1}:")
        for solution in maze_solutions:
            algorithm, steps, execution_time = solution
            print(f"Algorithm: {algorithm}")
            print(f"Steps: {steps}")
            print(f"Execution time: {execution_time}\n")

    # Print average steps and execution time per algorithm
    algorithms = [
        "BFS",
        "DFS",
        "DLS",
        "A* Euclidean Heuristic",
        "A* Manhattan Heuristic",
        "Greedy BFS Euclidean Heuristic",
        "Greedy BFS Manhattan Heuristic",
    ]

    for algorithm in algorithms:
        steps = 0
        execution_time = 0
        count = 0
        for maze_solutions in solutions:
            for solution in maze_solutions:
                if solution[0] == algorithm:
                    steps += solution[1]
                    execution_time += solution[2]
                    count += 1
        print(f"Average steps for {algorithm}: {steps/count}")
        print(f"Average execution time for {algorithm}: {execution_time/count}\n")


if __name__ == "__main__":
    main()
