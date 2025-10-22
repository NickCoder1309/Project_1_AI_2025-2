from objects import Node
from a_star_search import expand_node
import heapq, random


def uniform_cost_search(problem):
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
                f_value = child.path_cost
                reached[child.get_state()] = child
                heapq.heappush(frontier, (f_value, random.random(), child))
