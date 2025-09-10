import pygame
from pygame.locals import *

from physicsobject import PhysicsObject
from paddle import Paddle
from VecMath import VectorMath

from math import cos, sin, atan, pi

RED_PADDLE_PATH = "Assets/Images/redbat.png"
BLACK_PADDLE_PATH = "Assets/Images/blackbat.png"
TABLE_PATH = "Assets/Images/table.png"

WHITE = (255, 255, 255)
PADDLE_SPEED = 50 # move to paddle.py if and only if we decide to do powerups or special abilities someday

class GameEngine:
    def __init__(self, fr: int, position: list, surface):
        self.ball = PhysicsObject(position, [100, 1], 5)
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
        self.ball.velocity[1] = self.ball.velocity[1] + self.ball.acceleration * self.dt

        self.ball.position[0] = self.ball.position[0] + self.ball.velocity[0] * self.dt
        self.ball.position[1] = self.ball.position[1] + self.ball.velocity[1] * self.dt

    
    def update_collision(self):
        if (self.ball.position[1] + 10) > 900:
            self.ball.velocity[1] = -self.ball.velocity[1]

        if (self.ball.position[0] - 10) < 0 or (self.ball.position[0] + 10) > 1600:
            self.ball.velocity[0] = -self.ball.velocity[0]

        if (self.ball.position[1] < 0):
            self.ball.velocity[1] *= -1
        
        if self.paddles[0].compute_dist_from_ball(self.ball.position) < 10 and self.paddles[0].compute_center_dist(self.ball.position) < 75 and self.ball.velocity[0] < 0:
            print(self.ball.velocity)
            (x, y) = VectorMath.scalar_mult(self.ball.velocity, -1)
            y = -y
            theta = self.paddles[0].angle if self.paddles[0].angle > 0 else 180 + self.paddles[0].angle # Angle between line and x-axis
            alpha = atan(-y/x) * 180 / pi # Angle between velocity vector and x-axis 
            beta = 90 + atan(-self.paddles[0].a) * 180 / pi # Angle between normal and x-axis
            print(f"v = ({x}, {y})")
            # print(self.paddles[0].a)
            # print(theta)
            print(alpha)
            print(beta)
            print(f"{-self.paddles[0].a}x")
            input(">   ")
        
        if self.paddles[1].compute_dist_from_ball(self.ball.position) < 10 and self.paddles[1].compute_center_dist(self.ball.position) < 75 and self.ball.velocity[0] > 0:
            self.ball.velocity[0] = -self.ball.velocity[0]

        if (self.ball.position[1] > 675 and self.ball.velocity[1] == abs(self.ball.velocity[1])):
            self.ball.velocity[1] *= -1

    
    def update_screen(self):
        self.surface.blit(self.table_image, self.table_image.get_rect(center = self.table_image.get_rect(center = [800, 775]).center))
        
        pygame.draw.circle(self.surface, WHITE, self.ball.position, 10)

        self.surface.blit(*self.paddles[0].rotate_center()) # The star unpacks the tuple as arguments
        self.surface.blit(*self.paddles[1].rotate_center())

        # print(self.paddles[0].angle)

        pygame.draw.line(self.surface, WHITE, (0, self.paddles[0].b), (500, self.paddles[0].a * 500 + self.paddles[0].b))
        pygame.draw.line(self.surface, WHITE, (1700, self.paddles[1].a * 1700 + self.paddles[1].b), (500, self.paddles[1].a * 500 + self.paddles[1].b))
        pygame.draw.line(self.surface, WHITE, self.ball.position, VectorMath.add(self.ball.position, VectorMath.scalar_mult(self.ball.velocity, 50/VectorMath.length(self.ball.velocity))))

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