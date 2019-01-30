import math

class Tanks:

    def __init__(self, otherX, otherY, otherHeading, otherTurretHeading, otherHealth=5, otherAmmo=10):
        self.tank_X = otherX
        self.tank_Y = otherY
        self.tank_heading = otherHeading
        self.tank_turret_heading = otherTurretHeading
        self.tank_health = otherHealth
        self.tank_ammo = otherAmmo

    def update(self, otherX, otherY, otherHeading, otherTurretHeading, otherHealth, otherAmmo):
        self.tank_X = otherX
        self.tank_Y = otherY
        self.tank_heading = otherHeading
        self.tank_turret_heading = otherTurretHeading
        self.tank_health = otherHealth
        self.tank_ammo = otherAmmo

    def get_hp(self):
        return self.tank_health

    def get_all(self):
        return(self.tank_X, self.tank_Y, self.tank_heading, self.tank_turret_heading, self.tank_health, self.tank_ammo)

    def get_distance(self, my_x, my_y):
        X = self.tank_X - my_x
        Y = self.tank_Y - my_y
        return math.sqrt((X*X) + (Y*Y))

    def get_heading(self):
        return self.tank_heading

    def heading_to(self, my_x, my_y):
        """returns heading TOWARDS the tank in degrees, in the POV of our tank """

        heading = float(math.atan2((self.tank_Y-my_y), (self.tank_X -my_x)))  # returns heading in radians
        heading = float(math.degrees(heading))
        heading = math.fabs(heading - 360) % 360
        return heading

    def looking_at_us(self, my_x, my_y):
        '''Returns true is the enemy tank is looking/aiming at us'''
        looking = float(math.atan2((my_y - self.tank_Y), (my_x - self.tank_X)))  # returns heading in radians
        looking = float(math.degrees(looking))
        loooking = math.fabs((looking - 360) % 360)
        '''The following if checks whether the enemy tank is aiming at us (+-5 degrees since it can still hit us)'''
        if (self.tank_turret_heading >= looking -5) and (self.tank_turret_heading <= looking + 5):
            return True
        else:
            return False


