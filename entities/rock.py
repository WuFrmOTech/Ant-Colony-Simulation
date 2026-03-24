'''
Create a Rock class to represent rocks in the Ant Colony Simulation project. Rocks will be obstacles that ants need to navigate around. 
'''
class Rock:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.width = 3
        self.height = 3