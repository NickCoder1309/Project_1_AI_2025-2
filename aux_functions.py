#Function to reconstruct the path from the initial position to the final position
def reconstruct_path(final_node):
    path = []
    current_node = final_node
    while current_node is not None:
        path.append(current_node.get_position())
        current_node = current_node.get_parent()
    path.reverse()
    return path
