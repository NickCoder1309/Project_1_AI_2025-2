from objects import Node, Matrix, Queue
from aux_functions import reconstruct_path

#Function to find possible solutions
def find_solutions(initial_pos, map):
    matrix = Matrix(map)
    queue = Queue()
    print("Initial Position:", initial_pos)
    node = Node(initial_pos, None)
    queue.enQueue(node)

    while not queue.is_empty():
        #Boolean to check if a sample was found
        found_sample = False
        if queue.size()%10000 == 0:
            print("Passing 10,000 nodes...")
        #The first node to go in, goes out
        node = queue.deQueue()
        #Get the position of the node
        i,j = node.get_position()

        #Check if there is a sample and add it to the node
        if matrix.get_number((i,j)) == 6:
            if node.is_collected((i,j)):
                pass
            else:
                node.add_sample()
                found_sample = True
                print("Found sample at ", (i,j))
                print("Total samples collected: ", node.get_samples())
                node.add_visited_sample((i,j))

        #Check if all samples have been collected
        if node.get_samples() == 3:
            print("All samples collected!")
            return reconstruct_path(node)

        for x,y in [(i,j-1),(i-1,j),(i+1,j),(i,j+1)]:
            #Check if the new position is within the map limits
            if x < 0 or x >= matrix.get_max_x() or y < 0 or y >= matrix.get_max_y():
                continue
            #If the node has not found a sample, it can't go back to the position it came from
            if not node.is_sample_found():
                if node.get_parent() != None and node.parent.get_position() == (x,y):
                    continue
            #Check if the new position is not a wall
            if matrix.get_number((x,y)) != 1:
                new_node = Node((x,y), node, list(node.get_visited_samples()), found_sample, node.get_samples(), node.get_acum_cost(), node.get_gasoline())
                queue.enQueue(new_node)
