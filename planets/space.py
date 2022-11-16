import math

class Planet:
    def __init__(self, coordinates, radius, speed_vector):
        self.coords = coordinates
        self.radius = radius
        self.vector = speed_vector
        self.lines = list()
        self.mass = ((4/3)*(radius**3)*math.pi)



