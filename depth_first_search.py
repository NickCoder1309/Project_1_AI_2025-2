from objects import Node
from a_star_search import expand_node


def depth_first_search(problem):
    node = Node(problem.initial, avaible_samples=list(problem.samples))
    frontier = problem.frontier
    reached = problem.reached

    frontier.append(node)

    while frontier:
        node = frontier.pop()

        is_goal = problem.check_state(node)
        if is_goal:
            return node

        for child in expand_node(node, problem):
            if child.get_state() not in reached:
                reached[child.get_state()] = child
                frontier.append(child)
