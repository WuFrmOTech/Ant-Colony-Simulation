import pygame 


class Render:
    def __init__(self, screen):
        self.screen = screen

    def draw(self,env):
        self.screen.fill((0,0,0))

        #Origin/entry point
        pygame.draw.circle(self.screen, (0,255,0), (int(env.origin_x), int(env.origin_y)),30)
        pygame.draw.circle(self.screen, (0, 255, 0), (500, 400), 30)
        pygame.draw.circle(self.screen, (0, 0, 0), (500, 400), 30, 3)

        #Draw nats
        for ant in env.ants:
            pygame.draw.circle(self.screen, (255,255,255), (int(ant.x), int(ant.y)),3)