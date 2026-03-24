import pygame 

class Render:
    def __init__(self, screen):
        self.screen = screen

    def draw(self,env):
        self.screen.fill((0,0,0))

        #Draw grid
        for row in range(env.rows):
            for col in range(env.cols):
                cell = env.grid[row][col]

                if cell == "empty":
                    color = (255,255,255)
                elif cell == "dirt":
                    color = (168,112,78)
                elif cell == "rock":
                    color = (100,100,100)
                else:
                    color = (255,0,0)
                
                #Convert grid position to pixel position
                x = col * env.col_width
                y = row * env.row_height
        
                #Draw cell
                pygame.draw.rect(self.screen,color,(x, y, env.col_width, env.row_height))

        #Drwaw origin/entry point
        pygame.draw.circle(self.screen, (0,255,0), (int(env.origin_x), int(env.origin_y)),30)
        
        #Draw nats
        for ant in env.ants:
            pygame.draw.circle(self.screen, (255,255,255), (int(ant.x), int(ant.y)),3)