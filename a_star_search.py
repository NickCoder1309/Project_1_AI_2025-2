from objects import Node, Terrain
import heapq, random


def heuristic_function(node):
    x2, y2 = node.position

    mht_distances = []

    for sample_position in node.avaible_samples:
        x1, y1 = sample_position

        h = abs(x2 - x1) + abs(y2 - y1)

        mht_distances.append(h)

    return sum(mht_distances)


def a_star_search(problem):
    node = Node(problem.initial, avaible_samples=list(problem.samples))
    frontier = problem.frontier
    reached = problem.reached

    heapq.heappush(frontier, (0, random.random(), node))

    while frontier:
        _, _, node = heapq.heappop(frontier)

        is_goal = problem.check_state(node)
        if is_goal:
            return node

        for child in expand_node(node, problem):
            if (
                child.get_state() not in reached
                or child.path_cost < reached[child.get_state()].path_cost
            ):
                f_value = child.path_cost + heuristic_function(child)
                reached[child.get_state()] = child
                heapq.heappush(frontier, (f_value, random.random(), child))


def is_in_grid_bounds(position):
    x, y = position

    if x < 0 or x > 9 or y < 0 or y > 9:
        return False

    return True


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
