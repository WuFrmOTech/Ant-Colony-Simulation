'''
Stores everything for the simulation
'''

from entities.ant import Ant 

class Environment:
    def __init__(self, width, height):
        #Screen
        self.origin_x = width // 2
        self.origin_y = height // 2
        
        #Ants
        #self.ants = [Ant(self.origin_x, self.origin_y)]

        #ants 
        self.ants = [Ant(400, 300)]
