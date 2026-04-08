import math 

'''
A helper class that handels the ants movement
'''

class MovementSystem:
    '''
    Circle-circle collision
    '''
    @staticmethod
    def collides_with_rock(self, rock, new_x, new_y):
        dx = new_x - rock.x
        dy = new_y - rock.y
        distance = math.sqrt(dx * dx + dy * dy)

        return distance <= (self.radius + rock.radius)
    
    '''
    Keep ants inside the screen.
    '''
    @staticmethod
    def wall_collision(self, env, new_x, new_y):
        collided = False

        if new_x - self.radius < 0 or new_x + self.radius > env.width:
            self.vx *= -1
            collided = True

        if new_y - self.radius < 0 or new_y + self.radius > env.height:
            self.vy *= -1
            collided = True

        return collided
    
    '''
    Move the ant, but stop/redirect if rock collision.
    '''
    @staticmethod
    def move_with_collision(self, env):
        new_x = self.x + self.vx
        new_y = self.y + self.vy

        #irst check wall collision
        if self.wall_collision(env, new_x, new_y):
            return

        #check rock collisions
        for rock in env.rocks:
            if self.collides_with_rock(rock, new_x, new_y):
                # Collision response: choose a new random direction 
                self.choose_random_direction()
                return
            
        self.x = new_x
        self.y = new_y