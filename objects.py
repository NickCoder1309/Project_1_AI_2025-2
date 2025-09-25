from enum import Enum


class Terrain(Enum):
    FREE = 0
    WALL = 1
    ASTRONAUT = 2
    ROCKY = 3
    VOLCANIC = 4
    SPACESHIP = 5
    SAMPLE = 6


# Class for the Queus
class Queue:
    def __init__(self):
        self.queue = []

    def en_queue(self, item):
        self.queue.insert(0, item)

    def de_queue(self):
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
        samples=0,
        acum_cost=0,
        gasoline=0,
        heuristic_value=0,
    ):
        self.position = position
        self.parent = parent
        self.visited_samples = visited_samples if visited_samples is not None else []
        self.samples = samples
        self.acum_cost = acum_cost
        self.gasoline = gasoline
        self.heuristic_value = heuristic_value

    def __lt__(self, other):
        return self.acum_cost < other.acum_cost

    def get_acum_cost(self):
        return self.acum_cost

    def add_cost(self, cost):
        self.acum_cost += cost

    def add_sample(self):
        self.samples += 1

    def add_gasoline(self, gasoline):
        self.gasoline += gasoline

    def add_visited_sample(self, position):
        self.visited_samples.append(position)

    def set_heuristic_value(self, heuristic_value):
        self.heuristic_value = heuristic_value

    def already_collected(self, position):
        if self.visited_samples:
            for i, j in self.visited_samples:
                if (i, j) == position:
                    return True
            return False
        return False

    def get_f_value(self):
        return self.acum_cost + self.heuristic_value
