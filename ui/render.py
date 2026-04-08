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
                else:
                    color = (255,0,0)
                
                #Convert grid position to pixel position
                x = col * env.col_width
                y = row * env.row_height
        
                #Draw cell
                pygame.draw.rect(self.screen,color,(x, y, env.col_width, env.row_height))

        #Drwaw origin/entry point
        pygame.draw.circle(self.screen, (0,255,0), (int(env.home_x), int(env.home_y)),30)
        
        #Draw rocks
        for rock in env.rocks:
            pygame.draw.circle(self.screen, (100, 100, 100), (int(rock.x), int(rock.y)), rock.radius)

        #Draw food 
        for food in env.foods:
            if not food.found:
                pygame.draw.circle(self.screen, (0,0,255), (int(food.x), int(food.y)), food.radius) 
        
        #Draw nats
        for ant in env.ants:
            pygame.draw.circle(self.screen, (255,0,0), (int(ant.x), int(ant.y)), ant.radius)