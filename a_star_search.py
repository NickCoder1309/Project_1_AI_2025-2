from objects import Node, Terrain
from aux_functions import expand_node
import heapq, random


def heuristic_function(node):
    x2, y2 = node.position

    mht_distances = []

    for sample_position in node.avaible_samples:
        x1, y1 = sample_position

        h = abs(x2 - x1) + abs(y2 - y1)

        mht_distances.append(h)

    return min(mht_distances) + 20 - node.gasoline


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
