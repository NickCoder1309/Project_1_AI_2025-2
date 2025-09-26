from enum import Enum


class Problem:
    def __init__(self, grid, samples, initial):
        self.grid = grid
        self.samples = samples
        self.initial = initial
        self.frontier = []
        self.reached = set()

    def check_state(self, node):
        x, y = node.position

        terrain = Terrain(self.grid[x][y])

        is_goal = False

        if terrain == Terrain.SAMPLE:
            if node.is_already_collected((x, y)):
                pass
            else:
                self.reset_reached()
                node.collect_sample((x, y))
        elif terrain == Terrain.SPACESHIP:
            if node.is_spaceship_found():
                pass
            else:
                self.reset_reached()
                node.add_gasoline(20)
                node.spaceship_found()

        if not node.avaible_samples:
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
        avaible_samples=None,
        path_cost=0,
        gasoline=0,
        is_spaceship_found=False,
    ):
        self.position = position
        self.parent = parent
        self.avaible_samples = avaible_samples
        self.path_cost = path_cost
        self.gasoline = gasoline
        self.is_spaceship_found = is_spaceship_found

    def collect_sample(self, sample):
        self.avaible_samples.remove(sample)

    def is_already_collected(self, sample):
        if sample in self.avaible_samples:
            return False

        return True

    def spaceship_found(self):
        self.is_spaceship_found = True
