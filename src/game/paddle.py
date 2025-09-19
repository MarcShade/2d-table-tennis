import pygame
from pygame.locals import *
from math import sin, cos, pi, sqrt
from src.math.vector import Vector2

class Paddle:
    def __init__(self, px, py, path, player):
        self.MAX_ANGLE = 30
        self.MIN_ANGLE = -30
        self.SPEED = 50

        self.player = player

        self.angle = 0
        self.prev_angle = 0

        self.height = 150
        self.width = 150
        self.position = Vector2(px, py)
        
        self.key_set = set() # Keeping track of what keys are pressed

        self.image = pygame.transform.scale(pygame.image.load(path).convert_alpha(), (self.width, self.height))

        self.a = 0
        self.b = 0

    def update(self, fr):
        # Position
        if self.player == 1 and pygame.K_w in self.key_set:
            self.position.y -= self.SPEED * fr
        if self.player == 1 and pygame.K_s in self.key_set:
            self.position.y += self.SPEED * fr
        if self.player == 2 and pygame.K_UP in self.key_set:
            self.position.y -= self.SPEED * fr
        if self.player == 2 and pygame.K_DOWN in self.key_set:
            self.position.y += self.SPEED * fr

        # Rotation
        if self.player == 1 and pygame.K_a in self.key_set:
            self.angle += 15 * fr
        if self.player == 1 and pygame.K_d in self.key_set:
            self.angle += -15 * fr
        if self.player == 2 and pygame.K_LEFT in self.key_set:
            self.angle += 15 * fr
        if self.player == 2 and pygame.K_RIGHT in self.key_set:
            self.angle += -15 * fr

        self.angle = max(min(self.angle, self.MAX_ANGLE), self.MIN_ANGLE) # Clamping the angle
        
        if self.prev_angle != self.angle:
            self.prev_angle = self.angle
        # if pygame.K_KP_0 in self.key_set:
        #     print("Gotcha")

    def handle_input(self, key_set):
        self.key_set = key_set

    def draw(self, screen):
        screen.blit(*self.rotate_center())
    
    def rotate_center(self):
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        new_rect = rotated_image.get_rect(center = self.image.get_rect(center = tuple(self.position)).center)

        return (rotated_image, new_rect)

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