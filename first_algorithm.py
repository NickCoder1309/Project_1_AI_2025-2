from objects import Node, Queue
from aux_functions import reconstruct_path

#Function to find possible solutions
def find_solutions(initial_pos, map):
    matrix = map
    queue = Queue()
    print("Initial Position:", initial_pos)
    node = Node(initial_pos, None)
    queue.en_queue(node)

    while not queue.is_empty():
        #Boolean to check if a sample was found
        found_sample = False

        #The first node to go in, goes out
        node = queue.de_queue()

        #Get the position of the node
        i,j = node.position

        #Check if there is a sample and add it to the node
        if matrix[i][j] == 6:
            if node.already_collected((i,j)):
                pass
            else:
                node.add_sample()
                found_sample = True
                print("Found sample at ", (i,j))
                print("Total samples collected: ", node.samples)
                node.add_visited_sample((i,j))

        #Check if all samples have been collected
        if node.samples == 3:
            print("All samples collected!")
            return reconstruct_path(node)

        for x,y in [(i,j-1),(i-1,j),(i+1,j),(i,j+1)]:

            #Check if the new position is within the map limits
            if x < 0 or x > 9 or y < 0 or y > 9:
                continue
            
            #If the node has not found a sample, it can't go back to the position it came from
            if not node.is_sample_found():
                if node.parent != None and node.parent.position == (x,y):
                    continue
            
            #Check if the new position is not a wall
            if matrix[x][y] != 1:
                new_node = Node((x,y), node, list(node.visited_samples), found_sample, node.samples, node.gasoline)
                queue.en_queue(new_node)
