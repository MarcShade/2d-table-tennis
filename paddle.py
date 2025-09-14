import pygame
from pygame.locals import *
from math import sin, cos, pi, sqrt
from vector import Vector2

MAX_ANGLE = 30
MIN_ANGLE = -30

class Paddle:
    def __init__(self, px, py, path):
        self.position = Vector2(px, py)
        self.angle = 0
        self.prev_angle = 0
        self.height = 150

        self.image = pygame.image.load(path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (150, self.height)) # The width is a magic number since I will neither be changing it or referencing it

        self.a = 0
        self.b = 0
    
    def rotate_center(self): # I cannot for the life of me begin the comprehend why the fuck this is necessary to rotate one simple image
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        new_rect = rotated_image.get_rect(center = self.image.get_rect(center = tuple(self.position)).center)

        return (rotated_image, new_rect)

    def change_angle(self, angle):
        self.angle += angle
        self.angle = max(min(self.angle, MAX_ANGLE), MIN_ANGLE) # Clamping the angle

    def compute_dist_from_ball(self, ball_pos):
        (_x, _y) = self.position
        x = _x + sin(self.angle * pi/180) * self.height/2
        y = _y + cos(self.angle * pi/180) * self.height/2

        try:
            self.a = (_y - y) / (_x - x)
        except ZeroDivisionError:
            self.a = 9999999
        self.b = y - self.a * x

        return abs(self.a*ball_pos.x+self.b-ball_pos.y)/sqrt(self.a * self.a + 1)
    
    def compute_center_dist(self, ball_pos):
        return sqrt((self.position.x - ball_pos.x) * (self.position.x - ball_pos.x) + (self.position.y - ball_pos.y) * (self.position.y - ball_pos.y))