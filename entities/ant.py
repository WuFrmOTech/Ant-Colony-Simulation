import random
import math

'''
Creating the Ant class, which will represent the individual ants in the simulation.
Each ant has position, velocity, whether it is carrying food, and energy level.
'''
class Ant:
    def __init__(self, x, y, vx=0, vy=0, carrying_dirt=False, weight_Capacity=0, energy=100):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.carrying_dirt = carrying_dirt
        self.weight_Capacity = weight_Capacity
        self.energy = energy

        # Radius for drawing and circle-circle collision
        self.radius = 5
        self.speed = 2
        self.choose_random_direction()

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
        self.carrying_food = True

    def drop(self):
        self.carrying_food = False

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

    '''
    Circle-circle collision
    '''
    def collides_with_rock(self, rock, new_x, new_y):
        dx = new_x - rock.x
        dy = new_y - rock.y
        distance = math.sqrt(dx * dx + dy * dy)

        return distance <= (self.radius + rock.radius)

    '''
    Keep ants inside the screen.
    '''
    def wall_collision(self, env, new_x, new_y):
        collided = False

        if new_x - self.radius < 0 or new_x + self.radius > env.width:
            self.vx *= -1
            collided = True

        if new_y - self.radius < 0 or new_y + self.radius > env.height:
            self.vy *= -1
            collided = True

        return collided

    '''
    Move the ant, but stop/redirect if it collides with a rock.
    '''
    def move_with_collision(self, env):
        new_x = self.x + self.vx
        new_y = self.y + self.vy

        #irst check wall collision
        if self.wall_collision(env, new_x, new_y):
            return

        #check rock collisions
        for rock in env.rocks:
            if self.collides_with_rock(rock, new_x, new_y):
                # Collision response: choose a new random direction 
                self.choose_random_direction()
                return
            
        self.x = new_x
        self.y = new_y

    def get_grid_pos(self, env):
        col = int(self.x // env.col_width)
        row = int(self.y // env.row_height)
        return row, col

    def excavate(self, env):
        row, col = self.get_grid_pos(env)

        if 0 <= row < env.rows and 0 <= col < env.cols:
            if env.grid[row][col] == "dirt":
                env.grid[row][col] = "empty"
                self.carrying_dirt = True

    '''
    Random walk for continuous movement.
    '''
    def random_walk(self, env):
        #Small chance to change direction at each frame
        if random.random() < 0.05:
            self.choose_random_direction()

        self.move_with_collision(env)
        self.excavate(env)