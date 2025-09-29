# Importing Search algorithm
from breadth_first_search import breadth_first_search
from uniform_cost_search import uniform_cost_search
from depth_first_search import depth_first_search
from a_star_search import a_star_search
from aux_functions import reconstruct_path
from objects import Problem, Terrain


def load_map(filename):
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


grid, samples, initial = load_map("tests/Prueba1.txt")
problem = Problem(grid, samples, initial)

option = input(
    "Selecciona un algoritmo: \n 1. Búsqueda No Informada Preferente por Amplitud \n 2. Búsqueda No Informada de Costo Uniforme \n 3.Búsqueda No Informada por Profundidad  \n 4.Búsqueda A* \n 1 o 2 o 3 o 4 -> "
)
if option == "1":
    solution_node = breadth_first_search(problem)
elif option == "2":
    solution_node = uniform_cost_search(problem)
elif option == "3":
    solution_node = depth_first_search(problem)
elif option == "4":
    solution_node = a_star_search(problem)

print(reconstruct_path(solution_node))
