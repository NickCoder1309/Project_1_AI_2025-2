from enum import Enum


class Problem:
    def __init__(self, map, samples, initial):
        self.map = map
        self.samples = samples
        self.initial = initial
        self.frontier = []
        self.reached = set()

    def check_state(self, node):
        x, y = node.position

        terrain = Terrain(self.map[x][y])

        is_goal = False

        if terrain == Terrain.SAMPLE:
            if node.already_collected((x, y)):
                pass
            else:
                self.reset_reached()
                node.add_sample((x, y))
        elif terrain == Terrain.SPACESHIP:
            if node.is_spaceship_found():
                pass
            else:
                self.reset_reached()
                node.add_gasoline(20)
                node.set_spaceship_found(True)

        if node.samples == 3:
            is_goal = True

        return is_goal

    def reset_reached(self):
        self.reached = set()


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
        samples=None,
        path_cost=0,
        gasoline=0,
    ):
        self.position = position
        self.parent = parent
        self.samples = samples
        self.path_cost = path_cost
        self.gasoline = gasoline

    def add_sample(self, sample):
        self.samples.append(sample)

    def is_already_collected(self, sample):
        if sample in self.samples:
            return True

        return False
