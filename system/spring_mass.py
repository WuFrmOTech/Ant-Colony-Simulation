import math

class SpringMassSystem:
    @staticmethod
    def update(ant, dt=1.0):
        #Positions
        x_a, y_a = ant.x, ant.y                  
        x_m, y_m = ant.load_x, ant.load_y       

        #Velocities
        v_ax, v_ay = ant.vx, ant.vy              
        v_mx, v_my = ant.load_vx, ant.load_vy    

        #Masses
        m_a = ant.body_mass
        m_m = ant.load_mass

        #Spring parameters
        k = ant.spring_k
        c = ant.damping_c
        L0 = ant.spring_rest_length

        dx = x_m - x_a
        dy = y_m - y_a
        distance = math.sqrt(dx * dx + dy * dy)

        if distance < 1e-6:
            distance = 1e-6

        #Unit direction vector
        ux = dx / distance
        uy = dy / distance

        #Hookes law
        extension = distance - L0

        #Spring force 
        F_spring = -k * extension

        #Dampening force
        dvx = v_mx - v_ax
        dvy = v_my - v_ay

        #Project relative velocity onto spring direction
        v_rel = dvx * ux + dvy * uy

        F_damping = -c * v_rel

        F_total = F_spring + F_damping

        Fx = F_total * ux
        Fy = F_total * uy

        #Load mass acceleration
        if m_m > 0:
            a_mx = Fx / m_m
            a_my = Fy / m_m

            #Update load velocity
            ant.load_vx += a_mx * dt
            ant.load_vy += a_my * dt

            #update load position
            ant.load_x += ant.load_vx * dt
            ant.load_y += ant.load_vy * dt

        #Ant acceleration
        a_ax = -Fx / m_a
        a_ay = -Fy / m_a

        ant.vx += a_ax * dt
        ant.vy += a_ay * dt

    @staticmethod
    def reset_load(ant):
        ant.load_x = ant.x
        ant.load_y = ant.y
        ant.load_vx = 0
        ant.load_vy = 0
        ant.load_mass = ant.base_load_mass