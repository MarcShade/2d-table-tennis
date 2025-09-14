import pygame
from pygame.locals import *

from ball import Ball
from paddle import Paddle
from vector import Vector2

from math import cos, sin, atan, pi

RED_PADDLE_PATH = "Assets/Images/redbat.png"
BLACK_PADDLE_PATH = "Assets/Images/blackbat.png"
TABLE_PATH = "Assets/Images/table.png"

WHITE = (255, 255, 255)
PADDLE_SPEED = 50 # move to paddle.py if and only if we decide to do powerups or special abilities someday

class GameEngine:
    def __init__(self, fr: int, position: Vector2, surface):
        self.ball = Ball(position, Vector2(100, 1), 5, 10)
        self.dt = 1/fr
        self.paddles = [Paddle(100, 700, RED_PADDLE_PATH), Paddle(1500, 700, BLACK_PADDLE_PATH)]
        self.surface = surface
        self.running = True
        self.key_set = set() # Keeping track of what keys are pressed, because Pygame and I are opps

        self.table_image = pygame.image.load(TABLE_PATH).convert_alpha()
        self.table_image = pygame.transform.scale(self.table_image, (1000, 500))

    def update(self):
        self.handle_input()
        self.update_position()
        self.update_collision()
        self.update_screen()

        if self.paddles[0].prev_angle != self.paddles[0].angle:
            self.paddles[0].prev_angle = self.paddles[0].angle

    def update_position(self):
        # gravity
        self.ball.velocity.y = self.ball.velocity.y + self.ball.acceleration * self.dt

        self.ball.position = self.ball.position + self.ball.velocity * self.dt


    
    def update_collision(self):
        if (self.ball.position.y + 10) > 900:
            self.ball.velocity[1] *= -1

        if (self.ball.position.x - 10) < 0 or (self.ball.position.x + 10) > 1600:
            self.ball.velocity.x *= -1

        if (self.ball.position.y < 0):
            self.ball.velocity.y *= -1
        
        if self.paddles[0].compute_dist_from_ball(self.ball.position) < 10 and self.paddles[0].compute_center_dist(self.ball.position) < 75 and self.ball.velocity.x < 0:
            _beta = atan(1 / -self.paddles[0].a) * 180 / pi
            beta = _beta if _beta < 90 else -180 + _beta
            beta = beta * pi / 180
            
            self.ball.velocity = Vector2(cos(beta), sin(beta)) * self.ball.velocity.length()

        
        if self.paddles[1].compute_dist_from_ball(self.ball.position) < 10 and self.paddles[1].compute_center_dist(self.ball.position) < 75 and self.ball.velocity.x > 0:
            _beta = atan(1 / -self.paddles[1].a) * 180 / pi
            beta = 180 + _beta if _beta < 90 else 360 - _beta
            beta = beta * pi / 180

            self.ball.velocity = Vector2(cos(beta), sin(beta)) * self.ball.velocity.length()

        if (self.ball.position.y > 675 and self.ball.velocity.y == abs(self.ball.velocity.y)):
            self.ball.velocity.y *= -1

    
    def update_screen(self):
        self.surface.blit(self.table_image, self.table_image.get_rect(center = self.table_image.get_rect(center = [800, 775]).center))
        
        # pygame.draw.circle(self.surface, WHITE, tuple(self.ball.position), self.ball.radius)

        self.surface.blit(*self.paddles[0].rotate_center()) # The star unpacks the tuple as arguments
        self.surface.blit(*self.paddles[1].rotate_center())
        self.surface.blit(*self.ball.get_image())

        

        pygame.draw.line(self.surface, WHITE, (0, self.paddles[0].b), (500, self.paddles[0].a * 500 + self.paddles[0].b))
        pygame.draw.line(self.surface, WHITE, (1700, self.paddles[1].a * 1700 + self.paddles[1].b), (500, self.paddles[1].a * 500 + self.paddles[1].b))

    def handle_input(self):
        # Position
        if pygame.K_w in self.key_set:
            self.paddles[0].position.y -= PADDLE_SPEED * self.dt
        
        if pygame.K_s in self.key_set:
            self.paddles[0].position.y += PADDLE_SPEED * self.dt

        if pygame.K_UP in self.key_set:
            self.paddles[1].position.y -= PADDLE_SPEED * self.dt
        
        if pygame.K_DOWN in self.key_set:
            self.paddles[1].position.y += PADDLE_SPEED * self.dt

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