import pygame

from pygame.locals import *
from src.utils.math.vector import Vector2
from src.game.engine import GameEngine

from math import sin, cos, pi, sqrt, atan
from time import time

class Paddle:
    def __init__(self, px, py, path, player):
        self.MAX_ANGLE = 30
        self.MIN_ANGLE = -30
        self.SPEED = 50

        self.player = player
        self.time_since_last_hit = 0

        self.angle = 0
        self.prev_angle = 0
        self.outgoing_velocity = 0

        self.height = 150
        self.width = 150
        self.position = Vector2(px, py)
        
        self.key_set = set() # Keeping track of what keys are pressed
        self.allow_input = True
        self.frames = 0 # For animation purposes
        self.saved_position = None
        self.delay = 0.5

        self.image = pygame.transform.scale(pygame.image.load(path).convert_alpha(), (self.width, self.height))

        self.a = 0
        self.b = 0

    def update(self, fr):
        if self.allow_input == False:
            self.animate()
            return
        
        # Position
        if self.player == 1 and pygame.K_w in self.key_set:
            self.position.y -= self.SPEED * fr
        if self.player == 1 and pygame.K_s in self.key_set:
            self.position.y += self.SPEED * fr
        if self.player == 2 and pygame.K_UP in self.key_set:
            self.position.y -= self.SPEED * fr
        if self.player == 2 and pygame.K_DOWN in self.key_set:
            self.position.y += self.SPEED * fr

        self.position.y = max(min(self.position.y, GameEngine.window_size[1] - self.height/2), 0 + self.height/2)

        # Rotation
        if self.player == 1 and pygame.K_a in self.key_set:
            self.angle += 15 * fr
        if self.player == 1 and pygame.K_d in self.key_set:
            self.angle += -15 * fr
        if self.player == 2 and pygame.K_LEFT in self.key_set:
            self.angle += 15 * fr
        if self.player == 2 and pygame.K_RIGHT in self.key_set:
            self.angle += -15 * fr

        self.angle = max(min(self.angle, self.MAX_ANGLE), self.MIN_ANGLE)
        
        if self.prev_angle != self.angle:
            self.prev_angle = self.angle

        # Animation
        if time() - self.time_since_last_hit > self.delay:
            if self.player == 1 and pygame.K_SPACE in self.key_set:
                self.time_since_last_hit = time()
                self.animate()
            
            if self.player == 2 and pygame.K_RSHIFT in self.key_set:
                self.time_since_last_hit = time()
                self.animate()
    
    def compute_normal(self):
        if self.player == 1:
            _beta = atan(1 / -self.a) * 180 / pi
            beta = _beta if _beta < 90 else -180 + _beta
            beta = beta * pi / 180

        elif self.player == 2:
            _beta = atan(1 / -self.a) * 180 / pi
            beta = 180 + _beta if _beta < 90 else 360 - _beta
            beta = beta * pi / 180
        else:
            raise Exception("Not a valid value for the attribute self.player of Paddle")
        
        return Vector2(cos(beta), sin(beta))

    def reset(self):
        if self.player == 1:
            self.position = Vector2(100, 600)
            self.angle = 0
            self.outgoing_velocity = 0.5

        elif self.player == 2:
            self.position = Vector2(1500, 600)
            self.angle = 0
            self.outgoing_velocity = 0.5

        else:
            raise Exception("Not a valid value for the attribute self.player of Paddle")

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
    
    def animate(self):
        if self.frames == 0:
            self.allow_input = False
            self.saved_position = self.position
        self.position = self.position + 2 * self.compute_normal()
        self.frames += 1

        if self.frames == 60:
            self.frames = 0
            self.allow_input = True
            self.position = self.saved_position
            print("Done with animating")
