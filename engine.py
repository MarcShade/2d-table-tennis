import pygame
from pygame.locals import *

from physicsobject import PhysicsObject
from paddle import Paddle

from math import sin, cos, pi

RED_PADDLE_PATH = "Assets/Images/redbat.png"
BLACK_PADDLE_PATH = "Assets/Images/blackbat.webp"

WHITE = (255, 255, 255)
PADDLE_SPEED = 50 # move to paddle.py if and only if we decide to do powerups or special abilities someday

class GameEngine:
    def __init__(self, fr: int, position: list, surface):
        self.ball = PhysicsObject(position, [100, 1], 5)
        self.dt = 1/fr
        self.paddles = [Paddle(100, 700, RED_PADDLE_PATH), Paddle(1450, 700, BLACK_PADDLE_PATH)]
        self.surface = surface
        self.running = True
        self.key_set = set() # Keeping track of what keys are pressed, because Pygame and I are opps

    def update(self):
        self.handle_input()
        self.update_position()
        self.update_collision()
        self.update_screen()

        if self.paddles[0].prev_angle != self.paddles[0].angle:
            self.paddles[0].prev_angle = self.paddles[0].angle

    def update_position(self):
        # gravity
        self.ball.velocity[1] = self.ball.velocity[1] + self.ball.acceleration * self.dt

        self.ball.position[0] = self.ball.position[0] + self.ball.velocity[0] * self.dt
        self.ball.position[1] = self.ball.position[1] + self.ball.velocity[1] * self.dt
    
    def update_collision(self):
        if (self.ball.position[1] + 10) > 900:
            self.ball.velocity[1] = -self.ball.velocity[1]

        if (self.ball.position[0] - 10) < 0 or (self.ball.position[0] + 10) > 1600:
            self.ball.velocity[0] = -self.ball.velocity[0]
        
        if self.paddles[0].compute_dist_from_ball(self.ball.position) < 10 and self.paddles[0].compute_center_dist(self.ball.position) < 75 and self.ball.velocity[0] < 0:
            self.ball.velocity[0] = -self.ball.velocity[0]
        
        if self.paddles[1].compute_dist_from_ball(self.ball.position) < 10 and self.paddles[1].compute_center_dist(self.ball.position) < 75 and self.ball.velocity[0] > 0:
            self.ball.velocity[0] = -self.ball.velocity[0]

    
    def update_screen(self):
        pygame.draw.circle(self.surface, WHITE, self.ball.position, 10)

        self.surface.blit(*self.paddles[0].rotate_center()) # The star unpacks the tuple as arguments
        self.surface.blit(*self.paddles[1].rotate_center())

        pygame.draw.line(self.surface,  WHITE,  (0, self.paddles[0].b), (500, self.paddles[0].a * 500 + self.paddles[0].b))
        pygame.draw.line(self.surface,  WHITE,  (1700, self.paddles[1].a * 1700 + self.paddles[1].b), (500, self.paddles[1].a * 500 + self.paddles[1].b))

        print((0, self.paddles[1].b), (500, self.paddles[1].a * 500 - self.paddles[1].b))




    def handle_input(self):
        # Position
        if pygame.K_w in self.key_set:
            self.paddles[0].position[1] -= PADDLE_SPEED * self.dt
        
        if pygame.K_s in self.key_set:
            self.paddles[0].position[1] += PADDLE_SPEED * self.dt

        if pygame.K_UP in self.key_set:
            self.paddles[1].position[1] -= PADDLE_SPEED * self.dt
        
        if pygame.K_DOWN in self.key_set:
            self.paddles[1].position[1] += PADDLE_SPEED * self.dt

        # Rotation
        if pygame.K_a in self.key_set:
            self.paddles[0].change_angle(0.1)

        if pygame.K_d in self.key_set:
            self.paddles[0].change_angle(-0.1)
        
        if pygame.K_LEFT in self.key_set:
            self.paddles[1].change_angle(0.1)

        if pygame.K_RIGHT in self.key_set:
            self.paddles[1].change_angle(-0.1)
        
        # if pygame.K_KP_0 in self.key_set:
        #     print("Gotcha")