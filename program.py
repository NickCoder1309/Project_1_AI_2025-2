# Importing Search algorithm
from first_algorithm import find_solutions
from second_algorithm import find_solutions_2
from a_star_search import a_star_search
from objects import Problem


def load_map(filename):
    map = []
    samples = []
    initial = None

    with open(filename, "r") as f:
        for i, line in enumerate(f):
            row = list(map(int, line.strip().split()))
            map.append(row)
            for j, value in enumerate(row):
                if value == 2:
                    initial = (i, j)

                if value == 6:
                    samples.append((i, j))

    return map, samples, initial


map, samples, initial = load_map("tests/Prueba1.txt")
problem = Problem(map, samples, initial)

numero_algoritmo = input(
    "Selecciona un algoritmo: \n 1. Búsqueda No Informada Preferente por Amplitud \n 2. Búsqueda No Informada de Costo Uniforme \n 3. Búsqueda No Informada de Costo Uniformen 1 o 2 -> "
)
if numero_algoritmo == "1":
    solution_node = breadth_first_search(problem)
elif option == "2":
    solution_node = uniform_cost_search(problem)
elif option == "3":
    solution_node = a_star_search(problem)
