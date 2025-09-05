import pygame
from pygame.locals import *

from physicsobject import PhysicsObject
from paddle import Paddle

WHITE = (255, 255, 255)
PADDLE_SPEED = 25 # move to paddle.py if and only if we decide to do powerups or special abilities someday

class GameEngine:
    def __init__(self, fr: int, position: list, surface):
        self.ball = PhysicsObject(position, [50, 1], 10)
        self.dt = 1/fr
        self.paddles = [Paddle(30, 700, 5, 100), Paddle(1570, 700, 5, 100)]
        self.surface = surface
        self.running = True
        self.key_set = set() # Keeping track of what keys are pressed, because Pygame and I are opps


    def update(self):
        self.handle_input()
        self.update_position()
        self.update_collision()
        self.update_screen()

    def update_position(self):
        # gravity
        self.ball.velocity[1] = self.ball.velocity[1] + self.ball.acceleration * self.dt

        self.ball.position[0] = self.ball.position[0] + self.ball.velocity[0] * self.dt
        self.ball.position[1] = self.ball.position[1] + self.ball.velocity[1] * self.dt
    
    def update_collision(self):
        if (self.ball.position[1] + 10) > 900:
            self.ball.velocity[0] = self.ball.velocity[0]
            self.ball.velocity[1] = -self.ball.velocity[1]

        if (self.ball.position[0] - 10) < 0 or (self.ball.position[0] + 10) > 1600:
            self.ball.velocity[0] = -self.ball.velocity[0]
            self.ball.velocity[1] = self.ball.velocity[1]
    
    def update_screen(self):
        pygame.draw.circle(self.surface, WHITE, self.ball.position, 10)
        pygame.draw.rect(self.surface, WHITE, (self.paddles[0].position[0], self.paddles[0].position[1], self.paddles[0].width, self.paddles[0].height))
        pygame.draw.rect(self.surface, WHITE, (self.paddles[1].position[0], self.paddles[1].position[1], self.paddles[1].width, self.paddles[1].height))

    def handle_input(self):
        if pygame.K_w in self.key_set:
            self.paddles[0].position[1] -= PADDLE_SPEED * self.dt
        
        if pygame.K_s in self.key_set:
            self.paddles[0].position[1] += PADDLE_SPEED * self.dt

        # Rotation can only be done on images

        if pygame.K_UP in self.key_set:
            self.paddles[1].position[1] -= PADDLE_SPEED * self.dt
        
        if pygame.K_DOWN in self.key_set:
            self.paddles[1].position[1] += PADDLE_SPEED * self.dt