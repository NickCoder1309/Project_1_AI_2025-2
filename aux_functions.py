from objects import Terrain, Node


def reconstruct_path(final_node):
    path = []
    current_node = final_node
    while current_node is not None:
        path.append(current_node.position)
        current_node = current_node.parent
    path.reverse()
    return path


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
        )

        yield new_node


def is_in_grid_bounds(position):
    x, y = position

    if x < 0 or x > 9 or y < 0 or y > 9:
        return False

    return True
