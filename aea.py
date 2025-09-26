# Importing Search algorithm
from first_algorithm import find_solutions
from second_algorithm import find_solutions_2
from a_star_search import a_star_search
from aux_functions import reconstruct_path
from objects import Problem


def load_grid(filename):
    grid = []
    samples = []
    initial = None

    with open(filename, "r") as f:
        for i, line in enumerate(f):
            row = list(map(int, line.strip().split()))
            grid.append(row)
            for j, value in enumerate(row):
                if value == 2:
                    initial = (i, j)

                if value == 6:
                    samples.append((i, j))

    return grid, samples, initial


grid, samples, initial = load_grid("tests/Prueba1.txt")
problem = Problem(grid, samples, initial)

solution_node = a_star_search(problem)
print(solution_node.path_cost)
print(solution_node.is_spaceship_found)
print(reconstruct_path(solution_node))
