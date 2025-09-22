# Class for the map
class Matrix:
    def __init__(self, map):
        self.map = map

    def is_there(self, number):
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if self.map[i][j] == number:
                    return True
        return False

    def get_number(self, position):
        i, j = position
        return self.map[i][j]

    def get_position(self, number):
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if self.map[i][j] == number:
                    return (i, j)
        return None

    def get_map(self):
        return self.map

    def change_pos(self, position, number):
        i, j = position
        self.map[i][j] = number

    def get_max_x(self):
        return len(self.map)

    def get_max_y(self):
        return len(self.map[0])


# Class for the Queus
class Queue:
    def __init__(self):
        self.queue = []

    def enQueue(self, item):
        self.queue.insert(0, item)

    def deQueue(self):
        if not self.queue:
            return None
        return self.queue.pop()

    def is_empty(self):
        return len(self.queue) == 0

    def size(self):
        return len(self.queue)


# Class for the Nodes
class Node:
    def __init__(
        self,
        position,
        parent=None,
        visited_samples=None,
        found_sample=False,
        samples=0,
        acum_cost=0,
        gasoline=0,
        found_spaceship=False,
    ):
        self.position = position
        self.parent = parent
        self.visited_samples = visited_samples if visited_samples is not None else []
        self.found_sample = found_sample
        self.samples = samples
        self.acum_cost = acum_cost
        self.gasoline = gasoline
        self.found_spaceship = found_spaceship

    def __lt__(self, other):
        return self.acum_cost < other.acum_cost

    def get_acum_cost(self):
        return self.acum_cost

    def add_cost(self, cost):
        self.acum_cost += cost

    def get_samples(self):
        return self.samples

    def get_position(self):
        return self.position

    def get_parent(self):
        return self.parent

    def add_sample(self):
        self.samples += 1

    def add_gasoline(self, gasoline):
        self.gasoline += gasoline

    def get_visited_samples(self):
        return self.visited_samples

    def add_visited_sample(self, position):
        self.visited_samples.append(position)

    def is_sample_found(self):
        return self.found_sample

    def is_spaceship_found(self):
        return self.found_spaceship

    def set_spaceship_found(self, found):
        self.found_spaceship = True

    def is_collected(self, position):
        if self.visited_samples:
            for i, j in self.visited_samples:
                if (i, j) == position:
                    return True
            return False
        return False

    def get_gasoline(self):
        return self.gasoline
