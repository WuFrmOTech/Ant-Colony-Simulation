import random 

'''
Creating the Ant class, which will represent the individual ants in the simulation. Each ant will have properties such as position, velocity, whether it is carrying food, and its energy level.
'''
class Ant:
    #velocity set to 0 for temp
    def __init__(self, x, y, vx=0,vy=0,carrying_food=False, weight_Capacity = 0, energy = 100):
        self.x = x
        self.y = y
        self.vx = vx                # velocity in x 
        self.vy = vy                # velocity in y 
        self.carrying_food = carrying_food
        self.weight_Capacity = weight_Capacity
        self.energy = energy
    
    #move based on velocity 
    def move(self):
        self.x += self.vx
        self.y += self.vy

    def set_velocity(self, vx, vy):
        self.vx = vx
        self.vy = vy

    def pick_up(self, food):
        self.carrying_food = True

    def drop(self):
        self.carrying_food = False

    def update_energy(self, amount):
        self.energy += amount
        if self.energy < 0:
            self.energy = 0

    '''
    Convert pixel location to grid
    '''
    def get_grid_pos(self, env):
       col = int(self.x//env.col_width)
       row = int(self.y//env.row_height)
       return row, col
    
    def move_cell(self, row, col, env):
        self.x = col * env.col_width + env.col_width//2
        self.y = row * env.row_height + env.row_height//2
    
    '''
    Random in grid formation 
    '''
    def random_walk(self, env):
        curr_row, curr_col = self.get_grid_pos(env)

        directions = [(-1,0),(1,0),(0,-1),(0,1)]
        d_row, d_col = random.choice(directions)

        new_row = curr_row + d_row
        new_col = curr_col + d_col

        #bounds 
        if not (0 <= new_row < env.rows and 0 <= new_col < env.cols):
            return
        
        cell = env.grid[new_row][new_col]

        if cell == "rock":
            return 
        elif cell == "empty":
            self.move_cell(new_row, new_col, env)
        elif cell == "dirt":
            env.grid[new_row][new_col] = "empty"
            self.move_cell(new_row, new_col, env)