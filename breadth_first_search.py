from objects import Node, Queue
from a_star_search import expand_node


# Function to find possible solutions
def breadth_first_search(problem):
    node = Node(problem.initial, avaible_samples=list(problem.samples))
    frontier = Queue()
    reached = problem.reached

    frontier.en_queue(node)
    while frontier:
        node = frontier.de_queue()

        is_goal = problem.check_state(node)
        if is_goal:
            return node

        for child in expand_node(node, problem):
            if child.get_state() not in reached:
                reached[child.get_state()] = child
                frontier.en_queue(child)
