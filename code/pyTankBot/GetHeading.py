
import math

def get_heading(tank1,tank2):

    """returns heading of the tank in degrees, assuming tank1, tank2 are dict"""

    x1,y1 = tank1["x"], tank2["y"]
    x2,y2 = tank2["x"], tank2["y"]
    heading = float(math.atan2((y2-y1)/(x2-x1))) #returns heading in radians
    heading = float(math.degrees(heading))
    heading = (heading-360)%360
    return abs(heading)

def is_turret_heading(tank1,tank2):

    """returns true if turret of tank1 is pointing at tank2"""


    if tank1[turret_heading] == GetHeading(tank1,tank2):
        return True
    else:
        return False

def is_turret_heading_close(tank1,tank2):


    """..."""

    if GetHeading(tank1,tank2)-5 < tank1[turret_heading] and tank1[turret_heading] < GetHeading(tank1,tank2)+5:
        return True
    else:
        return False

##every tank object
##heading towards us
