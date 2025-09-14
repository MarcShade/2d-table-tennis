from math import sqrt

class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __iter__(self):
        yield self.x
        yield self.y

    def __add__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x + other.x, self.y + other.y)
        return NotImplemented
    
    def __sub__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x - other.x, self.y - other.y)
        return NotImplemented
    
    def __mul__(self, scalar):
        # v * scalar
        if isinstance(scalar, (int, float)):
            return Vector2(self.x * scalar, self.y * scalar)
        return NotImplemented

    def __rmul__(self, scalar):
        return self.__mul__(scalar)
    
    def length(self):
        return sqrt(self.x * self.x + self.y * self.y)