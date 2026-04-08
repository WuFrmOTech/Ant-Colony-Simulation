import random
import math
from system.movement import MovementSystem
from system.spring_mass import SpringMassSystem

'''
Creating the Ant class, which will represent the individual ants in the simulation.
Each ant has position, velocity, whether it is carrying food, and energy level.
'''
class Ant:
    def __init__(self, x, y, home_x, home_y, vx=0, vy=0, carrying_dirt=False, weight_Capacity=0, energy=100):
        #Ant constants
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.carrying_dirt = carrying_dirt
        self.weight_Capacity = weight_Capacity
        self.energy = energy

        #home position
        self.home_x = home_x
        self.home_y = home_y

        #Ant state
        self.state = "searching"

        #How many dirt cells this ant has collected
        self.dirt_collected = 0
        self.max_dirt_capacity = 10

        #Radius for drawing and circle-circle collision
        self.radius = 5
        self.speed = 2
        self.choose_random_direction()

        #Spring connection constants
        #ant mass
        self.body_mass = 1.0

        #mass properties
        self.base_load_mass = 0.5
        self.load_mass = self.base_load_mass

        #Invisible load position
        self.load_x = self.x
        self.load_y = self.y

        #Invisible load velocity
        self.load_vx = 0.0
        self.load_vy = 0.0

        #Spring parameters
        self.spring_k = 0.15
        self.damping_c = 0.18
        self.spring_rest_length = 8.0

        #Mass added for dirt cell excavated
        self.mass_per_dirt = 0.8

    '''
    Move based on velocity
    '''
    def move(self):
        self.x += self.vx
        self.y += self.vy

    def set_velocity(self, vx, vy):
        self.vx = vx
        self.vy = vy

    def pick_up(self, food):
        self.carrying_dirt = True

    def drop(self):
        self.carrying_dirt = False

    def update_energy(self, amount):
        self.energy += amount
        if self.energy < 0:
            self.energy = 0

    '''
    Choose a random direction using an angle.
    '''
    def choose_random_direction(self):
        angle = random.uniform(0, 2 * math.pi)
        self.vx = self.speed * math.cos(angle)
        self.vy = self.speed * math.sin(angle)

    def get_grid_pos(self, env):
        col = int(self.x // env.col_width)
        row = int(self.y // env.row_height)
        return row, col

    def excavate(self, env, x, y):
        col = int(x // env.col_width)
        row = int(y // env.row_height)

        if 0 <= row < env.rows and 0 <= col < env.cols:
            if env.grid[row][col] == "dirt":
                env.grid[row][col] = "empty"
                self.carrying_dirt = True
                self.dirt_collected += 1

                self.load_mass = self.base_load_mass + self.dirt_collected * self.mass_per_dirt


                if self.dirt_collected >= self.max_dirt_capacity:
                    self.state = "returning"

    '''
    Random walk for continuous movement.
    '''
    def random_walk(self, env):
        #Small chance to change direction at each frame
        if random.random() < 0.02:
            self.choose_random_direction()

        MovementSystem.move_with_collision(self, env)

        for food in env.foods:
            if not food.found:
                dx = self.x - food.x
                dy = self.y - food.y
                distance = (dx ** 2 + dy ** 2) ** 0.5

                if distance <= food.radius + self.radius:
                    food.found = True
                    print("Food found")    

    '''
    Move to entry point
    '''
    def move_to_entry(self, env):
        dx = self.home_x - self.x
        dy = self.home_y - self.y
        distance = math.sqrt(dx * dx + dy * dy)

        if distance <= self.speed:
            self.x = self.home_x
            self.y = self.home_y
            self.drop()
            self.dirt_collected = 0
            self.load_mass = self.base_load_mass
            self.state = "searching"
            self.choose_random_direction()
            return
        
        self.vx = (dx / distance) * self.speed
        self.vy = (dy / distance) * self.speed
        MovementSystem.move_with_collision(self, env)

    '''
    Main method for ants 
    '''
    def update(self, env):  

        SpringMassSystem.update(self)

        if self.state == "searching":
            self.random_walk(env)
        elif self.state == "returning":
            self.move_to_entry(env)
        
