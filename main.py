from a_star_search import a_star_search
from aux_functions import reconstruct_path
from breadth_first_search import breadth_first_search
from depth_first_search import depth_first_search
from uniform_cost_search import uniform_cost_search
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

numero_algoritmo = input(
    "Selecciona un algoritmo: \n 1. Búsq. Por Amplitud \n 2. Búsq. Costo Uniforme \n 3. Búsq. Por Profundidad \n 4. A* \n 1 : 2 : 3 : 4 -> "
)
if numero_algoritmo == "1":
    solution_node = breadth_first_search(problem)
elif numero_algoritmo == "2":
    solution_node = uniform_cost_search(problem)
    print(solution_node.path_cost)
elif numero_algoritmo == "3":
    solution_node = depth_first_search(problem)
elif numero_algoritmo == "4":
    solution_node = a_star_search(problem)
    print(solution_node.path_cost)


print(reconstruct_path(solution_node))
