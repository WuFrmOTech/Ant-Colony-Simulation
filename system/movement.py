import math

'''
A helper class that handles the ants movement
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
    
    @staticmethod
    def collide_with_grid(self, env, new_x, new_y):
        col = int(new_x // env.col_width)
        row = int(new_y // env.row_height)

        if 0 <= row < env.rows and 0 <= col < env.cols:
            cell = env.grid[row][col]
            return cell == "rock" or cell == "dirt"
        
        return True

    '''
    Keep ants inside the screen.
    '''
    @staticmethod
    def wall_collision(self, env, new_x, new_y):
        collided = False

        if new_x - self.radius < 0 or new_x + self.radius > env.width:
            self.vx *= -1
            new_x = self.x + self.vx  # recompute

        if new_y - self.radius < 0 or new_y + self.radius > env.height:
            self.vy *= -1
            new_y = self.y + self.vy

        return collided

    '''
    Move the ant, but stop/redirect if rock collision.
    '''
    @staticmethod
    def move_with_collision(self, env):
        new_x = self.x + self.vx
        new_y = self.y + self.vy

                # check rock collisions
        for rock in env.rocks:
            if MovementSystem.collides_with_rock(self, rock, new_x, new_y):
                self.vx *= -0.5
                self.vy *= -0.5

                self.x += self.vx
                self.y += self.vy
                return

        # first check wall collision
        MovementSystem.wall_collision(self, env, new_x, new_y)
        
        #X-movement and collision for dirt
        if not MovementSystem.collide_with_grid(self, env, new_x, self.y):
            self.x = new_x
        else:
            col = int(new_x // env.col_width)
            row = int(self.y // env.row_height)

            if 0 <= row < env.rows and 0 <= col < env.cols:
                if env.grid[row][col] == "dirt":
                    self.excavate(env, new_x, self.y)
                    
            self.vx *= -0.3

        #Y-movement and collision for dirt
        if not MovementSystem.collide_with_grid(self, env, self.x, new_y):
            self.y = new_y
        else:
            col = int(self.x // env.col_width)
            row = int(new_y // env.row_height)

            if 0 <= row < env.rows and 0 <= col < env.cols:
                if env.grid[row][col] == "dirt":
                    self.excavate(env, self.x, new_y)

            self.vy *= -0.3

        # If stuck → pick new direction
        blocked_x = MovementSystem.collide_with_grid(self, env, new_x, self.y)
        blocked_y = MovementSystem.collide_with_grid(self, env, self.x, new_y)

        if blocked_x and blocked_y:
            self.choose_random_direction()


