from objects import Node, Terrain
import heapq, random


def heuristic_function(node):
    avaible_samples = list(node.avaible_samples)
    if not avaible_samples:
        return 0

    current_pos = node.position
    total = 0

    while avaible_samples:
        nearest_sample = min(
            avaible_samples,
            key=lambda s: abs(current_pos[0] - s[0]) + abs(current_pos[1] - s[1]),
        )
        nearest_dist = abs(current_pos[0] - nearest_sample[0]) + abs(
            current_pos[1] - nearest_sample[1]
        )

        total += nearest_dist
        current_pos = nearest_sample
        avaible_samples.remove(nearest_sample)

    if node.gasoline > 0:
        total *= 0.5

    return total


def greedy_search(problem):
    node = Node(problem.initial, avaible_samples=list(problem.samples))
    frontier = problem.frontier
    reached = problem.reached

    # f = h (no incluye costo del camino)
    heapq.heappush(frontier, (heuristic_function(node), random.random(), node))

    while frontier:
        _, _, node = heapq.heappop(frontier)

        if problem.check_state(node):
            return node

        for child in expand_node(node, problem):
            # solo reemplaza si el estado no se ha visitado
            if child.get_state() not in reached:
                reached[child.get_state()] = child
                f_value = heuristic_function(child)
                heapq.heappush(frontier, (f_value, random.random(), child))


def is_in_grid_bounds(position):
    x, y = position
    return 0 <= x <= 9 and 0 <= y <= 9


def expand_node(node, problem):
    i, j = node.position

    for x, y in [(i, j - 1), (i - 1, j), (i + 1, j), (i, j + 1)]:
        if not is_in_grid_bounds((x, y)):
            continue

        terrain = Terrain(problem.grid[x][y])

        if terrain in (
            Terrain.FREE,
            Terrain.ASTRONAUT,
            Terrain.SPACESHIP,
            Terrain.SAMPLE,
        ):
            cost = 1
        elif terrain == Terrain.ROCKY:
            cost = 3
        elif terrain == Terrain.VOLCANIC:
            cost = 5
        elif terrain == Terrain.WALL:
            continue
        else:
            continue

        gasoline_spent = 0
        if node.gasoline > 0:
            gasoline_spent = 1
            cost /= 2

        new_node = Node(
            (x, y),
            node,
            list(node.avaible_samples),
            node.path_cost + cost,
            node.gasoline - gasoline_spent,
            node.is_spaceship_found,
        )

        yield new_node
