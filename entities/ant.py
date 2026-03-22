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

    