# Importing Search algorithm
from first_algorithm import find_solutions
from second_algorithm import find_solutions_2


def load_map(filename):
    matrix = []
    start_pos = None

    with open(filename, "r") as f:
        for i, line in enumerate(f):
            row = list(map(int, line.strip().split()))
            matrix.append(row)
            for j, value in enumerate(row):
                if value == 2:  # posición inicial
                    start_pos = (i, j)

    return matrix, start_pos


map, start_pos = load_map("tests/Prueba1.txt")

numero_algoritmo = input(
    "Selecciona un algoritmo: \n 1. Búsqueda No Informada Preferente por Amplitud \n 2. Búsqueda No Informada de Costo Uniforme \n 1 o 2 -> "
)
if numero_algoritmo == "1":
    solution_node = find_solutions(start_pos, map)
    print("Solution Path:", solution_node)
else:
    solution_node = find_solutions_2(start_pos, map)
    print("Solution Path:", solution_node)
