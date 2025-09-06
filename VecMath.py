from math import acos, sqrt, pi

class VectorMath:
    @staticmethod
    def dot(a, b):
        return a[0] * b[0] + a[1] * b[1]
    
    @staticmethod
    def length(a):
        return sqrt(a[0] * a[0] + a[1] * a[1])
    
    @staticmethod
    def add(a, b):
        return [a[0] + b[0], a[1] + b[1]]
    
    @staticmethod
    def scalar_mult(a, k):
        return [a[0] * k, a[1] * k]
    
    @staticmethod
    def angle_between_two_vectors(a, b):
        return acos((VectorMath.dot(a, b)) / (VectorMath.length(a) * VectorMath.length(b))) * 180 / pi