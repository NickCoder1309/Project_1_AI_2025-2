from objects import Node, Queue
from aux_functions import reconstruct_path
import heapq


def find_solutions_2(initial_pos, map):
    matrix = map
    priorityQueue = []
    print("Initial Position:", initial_pos)
    node = Node(initial_pos, None)
    heapq.heappush(priorityQueue, (node.acum_cost, node))

    while priorityQueue:
        # Boolean to check if a sample was found
        found_sample = False

        # We extract the node with the lowest cost
        cost, node = heapq.heappop(priorityQueue)

        # Get the position of the node
        i, j = node.position

        # ACTIONS FOR THE ASTRONAUT
        # The astronaut can take the following actions once placed on a position

        # Check if there is a sample and add it to the node
        if matrix[i][j] == 6:
            if node.already_collected((i, j)):
                pass
            else:
                node.add_sample()
                found_sample = True
                print("Found sample at ", (i, j))
                print("Total samples collected: ", node.samples)
                node.add_visited_sample((i, j))
        # Check if there is a spaceship and if it hasn't been taken yet
        if matrix[i][j] == 5:
            if node.is_spaceship_found():
                pass
            else:
                node.add_gasoline(20)
                node.set_spaceship_found(True)

        # Check if all samples have been collected
        if node.samples == 3:
            print("All samples collected!")
            print("Total cost for this solution: ", node.acum_cost)
            return reconstruct_path(node)

        for x, y in [(i, j - 1), (i - 1, j), (i + 1, j), (i, j + 1)]:
            # Check if the new position is within the map limits
            if x < 0 or x > 9 or y < 0 or y > 9:
                continue

            # If the node has not found a sample, it can't go back to the position it came from
            if not node.is_sample_found():
                if node.parent != None and node.parent.position == (x, y):
                    continue

            # Check next position: 0=Free space, 1=Wall, 2=Astronaut, 3=Rocky ground, 4=Volcanic Ground, 5=Spaceship, 6=Sample
            if matrix[x][y] == 0:
                cost = 1
                gasoline_spent = 0
                if node.is_spaceship_found() and node.gasoline > 0:
                    gasoline_spent = 1
                    cost = 1 / 2
                new_node = Node(
                    (x, y),
                    node,
                    list(node.visited_samples),
                    found_sample,
                    node.samples,
                    node.acum_cost + cost,
                    node.gasoline - gasoline_spent,
                    node.is_spaceship_found(),
                )
                heapq.heappush(priorityQueue, (new_node.acum_cost, new_node))

            elif matrix[x][y] == 1:
                continue
            elif matrix[x][y] == 2:
                cost = 1
                gasoline_spent = 0
                if node.is_spaceship_found() and node.gasoline > 0:
                    gasoline_spent = 1
                    cost = 1 / 2
                new_node = Node(
                    (x, y),
                    node,
                    list(node.visited_samples),
                    found_sample,
                    node.samples,
                    node.acum_cost + cost,
                    node.gasoline - gasoline_spent,
                    node.is_spaceship_found(),
                )
                heapq.heappush(priorityQueue, (new_node.acum_cost, new_node))
            elif matrix[x][y] == 3:
                cost = 3
                gasoline_spent = 0
                if node.is_spaceship_found() and node.gasoline > 0:
                    gasoline_spent = 1
                    cost = 3 / 2
                new_node = Node(
                    (x, y),
                    node,
                    list(node.visited_samples),
                    found_sample,
                    node.samples,
                    node.acum_cost + cost,
                    node.gasoline - gasoline_spent,
                    node.is_spaceship_found(),
                )
                heapq.heappush(priorityQueue, (new_node.acum_cost, new_node))
            elif matrix[x][y] == 4:
                cost = 5
                gasoline_spent = 0
                if node.is_spaceship_found() and node.gasoline > 0:
                    gasoline_spent = 1
                    cost = 5 / 2
                new_node = Node(
                    (x, y),
                    node,
                    list(node.visited_samples),
                    found_sample,
                    node.samples,
                    node.acum_cost + cost,
                    node.gasoline - gasoline_spent,
                    node.is_spaceship_found(),
                )
                heapq.heappush(priorityQueue, (new_node.acum_cost, new_node))
            elif matrix[x][y] == 5:
                cost = 1
                gasoline_spent = 0
                if node.is_spaceship_found() and node.gasoline > 0:
                    gasoline_spent = 1
                    cost = 1 / 2
                new_node = Node(
                    (x, y),
                    node,
                    list(node.visited_samples),
                    found_sample,
                    node.samples,
                    node.acum_cost + cost,
                    node.gasoline - gasoline_spent,
                    True,
                )
                heapq.heappush(priorityQueue, (new_node.acum_cost, new_node))
            elif matrix[x][y] == 6:
                cost = 1
                gasoline_spent = 0
                if node.is_spaceship_found() and node.gasoline > 0:
                    gasoline_spent = 1
                    cost = 1 / 2
                new_node = Node(
                    (x, y),
                    node,
                    list(node.visited_samples),
                    found_sample,
                    node.samples,
                    node.acum_cost + cost,
                    node.gasoline - gasoline_spent,
                    node.is_spaceship_found(),
                )
                heapq.heappush(priorityQueue, (new_node.acum_cost, new_node))
