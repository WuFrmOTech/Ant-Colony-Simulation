'''
Creating the Ant class, which will represent the individual ants in the simulation. Each ant will have properties such as position, velocity, whether it is carrying food, and its energy level.
'''
class Ant:

    def __init__(self, x, y, velocity, carrying_food=False, weight_Capacity = 0, energy = 100):
        self.x = x
        self.y = y
        self.velocity = velocity
        self.carrying_food = carrying_food
        self.weight_Capacity = weight_Capacity
        self.energy = energy

    def move(self, dx, dy):
        pass

    def pick_up(self, food):
        pass

    def drop():
        pass

    def update_energy(self, amount):
        pass

    