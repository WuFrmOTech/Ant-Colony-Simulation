import random
import math

'''
Creating the Ant class, which will represent the individual ants in the simulation.
Each ant has position, velocity, whether it is carrying food, and energy level.
'''
class Ant:
    def __init__(self, x, y, vx=0, vy=0, carrying_dirt=False, weight_Capacity=5, energy=100):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.carrying_dirt = carrying_dirt
        self.weight_Capacity = weight_Capacity
        self.energy = energy

        self.weight = 0
        self.state = "searching"  # can be "searching", "returning", or "excavating"

        # Radius for drawing and circle-circle collision
        self.radius = 5
        self.base_speed = 2
        self.speed = self.base_speed
        self.choose_random_direction()

        self.return_cooldown = 0

    '''
    Move based on velocity
    '''
    def move(self):
        self.x += self.vx
        self.y += self.vy

    def set_velocity(self, vx, vy):
        self.vx = vx
        self.vy = vy

    def pick_up(self):
        if self.weight < self.weight_Capacity:
            self.weight += 1
            self.carrying_dirt = True

    def drop(self):
        self.carrying_dirt = False
        self.weight = 0

    def update_energy(self):
        cost = 0.1 + 0.05 * self.weight
        self.energy -= cost

        if self.energy < 0:
            self.energy = 0

    def update_speed(self):
        self.speed = max(0.5, self.base_speed - 0.2 * self.weight)

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
            if env.grid[row][col] == "dirt" and self.weight < self.weight_Capacity:
                env.grid[row][col] = "empty"
                self.pick_up()


    def move_to_entry(self, env):
        entry_x = env.origin_x
        entry_y = env.origin_y

        dx = entry_x - self.x
        dy = entry_y - self.y
        distance = math.sqrt(dx**2 + dy**2)

        if distance > 0:
            self.vx = self.speed * dx / distance
            self.vy = self.speed * dy / distance

        self.move_with_collision(env)

        # If close to entry -> drop load + reset
        if distance < 15:
            self.drop()
            self.energy = 100
            self.state = "searching"

            self.return_cooldown = 30   

            self.choose_random_direction()

            # FORCE movement away from center
            self.x += self.vx * 5
            self.y += self.vy * 5
                

    '''
    Random walk for continuous movement.
    '''
    def random_walk(self, env):
        self.update_speed()
        self.update_energy()

        # Reduce cooldown
        if self.return_cooldown > 0:
            self.return_cooldown -= 1

        # Only allow returning if cooldown is done
        if self.return_cooldown == 0:
            if self.weight >= self.weight_Capacity or self.energy < 20:
                self.state = "returning"

        if self.state == "searching":
            if random.random() < 0.05:
                self.choose_random_direction()

            self.move_with_collision(env)
            self.excavate(env)

        elif self.state == "returning":
            self.move_to_entry(env)