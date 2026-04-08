'''
This file contains the Food class for the Ant Colony Simulation project. The Food class represents the food sources in the simulation, which ants will seek out and collect.
'''

class Food:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.found = False
        
