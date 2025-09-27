from objects import Node, Queue, Terrain, Problem
from aux_functions import is_in_grid_bounds, expand_node


# Function to find possible solutions
def breadth_first_search(problem):
    node = Node(problem.initial, avaible_samples=list(problem.samples))
    frontier = problem.frontier
    reached = problem.reached

    frontier.insert(0, node)
    while frontier:
        node = frontier.pop()

        is_goal = problem.check_state(node)
        if is_goal:
            return node

        for child in expand_node(node, problem):
            if child.get_state() not in reached:
                reached[child.get_state()] = child
                frontier.insert(0, child)
