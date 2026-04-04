'''
Stores everything for the simulation
'''
import random
from entities.ant import Ant 
from entities.rock import Rock

class Environment:
    def __init__(self, width, height):
        self.width = width 
        self.height = height

        # Screen
        self.origin_x = width // 2
        self.origin_y = height // 2

        # Grid
        self.cols = 50
        self.rows = 40

        # Size of each cell in pixels
        self.col_width = width // self.cols
        self.row_height = height // self.rows
        self.grid = self.create_grid()

        # Entry point
        self.create_entry()

        # Ants
        spawn_x = self.entry_col * self.col_width + self.col_width // 2
        spawn_y = self.entry_row * self.row_height + self.row_height // 2
        self.ants = [Ant(spawn_x, spawn_y) for _ in range(10)]

        # Rocks
        self.rocks = []
        self.create_rocks(10)

    '''
    Creates the base environment grid.
    '''
    def create_grid(self):
        grid = []
        for row in range(self.rows):
            grid_row = []
            for col in range(self.cols):
                grid_row.append("dirt")
            grid.append(grid_row)
        return grid

    '''
    Randomly places circular rocks in the environment.
    '''
    def create_rocks(self, num_rocks):
        rocks = 0
        while rocks < num_rocks:
            radius = 40

            x = random.randint(radius, self.width - radius)
            y = random.randint(radius, self.height - radius)

            if self.can_place_rock(x, y, radius):
                rock = Rock(x, y, radius)
                self.rocks.append(rock)
                rocks += 1

    '''
    Checks whether a circular rock can be placed.
    Prevents overlap with the entry point and other rocks.
    '''
    def can_place_rock(self, x, y, radius):
        # Keep rocks away from the entry point
        dx = x - self.origin_x
        dy = y - self.origin_y
        distance = (dx ** 2 + dy ** 2) ** 0.5

        if distance < radius + 40:
            return False

        # Prevent overlap with existing rocks
        for rock in self.rocks:
            dx = x - rock.x
            dy = y - rock.y
            distance = (dx ** 2 + dy ** 2) ** 0.5

            if distance < radius + rock.radius:
                return False
        return True

    '''
    Creates an entry point for the environment and ants.
    '''
    def create_entry(self):
        self.entry_col = self.origin_x // self.col_width
        self.entry_row = self.origin_y // self.row_height
        self.entry_cell = (self.entry_row, self.entry_col)

        self.grid[self.entry_row][self.entry_col] = "empty"

    '''
    Update position for ants
    '''
    def update(self):
        for ant in self.ants:
            ant.random_walk(self)