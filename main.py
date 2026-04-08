import pygame
from system.environment import Environment
from ui.render import Render

# Constants for screen
width = 1000
height = 800

'''
Create pygame window
'''
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Ant Colony Simulation")
clock = pygame.time.Clock()

#Creat enviroment for simulation
env = Environment(width,height)
renderer = Render(screen)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
    
    if env.running:
        env.update()

    renderer.draw(env)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()