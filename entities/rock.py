'''
Create a Rock class to represent rocks in the Ant Colony Simulation project. Rocks will be obstacles that ants need to navigate around. 
'''
class Rock:
    def __init__(self, x, y, radius=40):
        self.x = x
        self.y = y
        self.radius = radius