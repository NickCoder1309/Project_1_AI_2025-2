from objects import Node, Terrain
from aux_functions import reconstruct_path
import heapq


def heuristic_function(pos, valid_samples):
    mht_distances = []

    for x, y in valid_samples:
        h = abs(pos[0] - x) + abs(pos[1] - y)

        mht_distances.append(h)

    return min(mht_distances)


def a_star_search(initial_pos, map, samples):
    node = Node(initial_pos)
    frontier = []
    reached = set()

    heapq.heappush(frontier, (0, node))

    while priorityQueue:
        _, node = heapq.heappop(priorityQueue)

        i, j = node.position

        if node.samples == 3:
            return node

        if map[i][j] == 6:
            if node.already_collected((i, j)):
                pass
            else:
                node.add_sample()
                found_sample = True
                node.add_visited_sample((i, j))

        if map[i][j] == 5:
            if node.is_spaceship_found():
                pass
            else:
                node.add_gasoline(20)
                node.set_spaceship_found(True)

        for child in expand_node(node, map, samples):
            if child not in reached:
                reached.add(child)
                heapq.heappush(frontier, (child.get_f_value, child))


def is_in_map_bounds(position):
    x, y = position

    if x < 0 or x > 9 or y < 0 or y > 9:
        return False

    return True


def expand_node(node, map, samples):
    i, j = node.position

    for x, y in [(i, j - 1), (i - 1, j), (i + 1, j), (i, j + 1)]:
        if not is_in_map_bounds((x, y)):
            continue

        terrain = Terrain(map[x][y])

        terrain = Terrain(map[x][y])

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

        heuristic_value = heuristic_function((x, y), samples)

        new_node = Node(
            (x, y),
            node,
            list(node.visited_samples),
            node.samples,
            node.acum_cost + cost,
            node.gasoline - gasoline_spent,
            heuristic_value,
        )

        yield new_node
