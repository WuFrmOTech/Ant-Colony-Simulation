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

        #Screen
        self.origin_x = width // 2
        self.origin_y = height // 2

        #Grid 
        self.cols = 50
        self.rows = 40

        #Size of each cell in pixels
        self.col_width = width//self.cols
        self.row_height = height//self.rows
        self.grid = self.create_grid()

        #Entry point 
        self.create_entry()
        
        #Ants 
        self.ants = [Ant(self.entry_col * self.col_width + self.col_width // 2, 
                         self.entry_row * self.row_height + self.row_height // 2) 
                         for _ in range(10)]

        
        #Rocks
        self.rocks = []
        self.create_rocks(8)
    
    '''
    Creates the base environment grid.
    Top rows = EMPTY (surface area / nest entrance)
    Bottom rows = DIRT (area to excavate)
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
    Randomly places a fixed number of rocks in the grid.
    Each rock is 2x2 cells.
    '''
    def create_rocks(self, num_rocks):
        rocks = 0
        while rocks < num_rocks:
            #Random top-left position for the rock
            #-3 ensures the 2x2 rock fits inside bounds
            start_row = random.randint(0,self.rows-3)
            start_col = random.randint(0,self.cols-3)

            #Only place rock if space is valid
            if self.can_place(start_row, start_col):
                rock = Rock(start_row, start_col)
                self.rocks.append(rock)
                #Place rock if dirt 
                self.place_rock(rock)
                rocks += 1 

    '''
    Checks if a 2x2 rock can be placed at a given location.
    Ensures:
    no overlap with other rocks and no placement in an empty space
    '''
    def can_place(self,start_row, start_col):
        for row in range(start_row, start_row+2):
            for col in range(start_col, start_col+2):
                #If any cell is not DIRT, placement is invalid
                if self.grid[row][col] != "dirt":
                    return False
        return True 
    
    '''
    Converts the cells covered by the rock into rock.
    '''
    def place_rock(self, rock):
        for row in range(rock.row, rock.row + rock.height):
            for col in range(rock.col, rock.col + rock.width):
                self.grid[row][col] = "rock"

    '''
    Creates an entry point for the environment and ants.
    '''
    def create_entry(self):
        self.entry_col = self.origin_x//self.col_width
        self.entry_row = self.origin_y//self.row_height
        self.entry_cell = (self.entry_row, self.entry_col)

        self.grid[self.entry_row][self.entry_col] = "empty"

    '''
    Update position for ants
    '''
    def update(self):
        for ants in self.ants:
            ants.random_walk(self)