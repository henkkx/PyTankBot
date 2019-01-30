import math

def calculate_distance(ownX, ownY, otherX, otherY):
    headingX = otherX - ownX
    headingY = otherY - ownY

    return math.sqrt(headingX**2 + headingY**2)

