from src.math.vector import Vector2
import pygame
from pygame.locals import *

IMAGE_PATH = "assets/textures/ball.png"

class Ball:
    def __init__(self, initial_position: Vector2, initial_velocity: Vector2, acceleration: int):
        self.position = initial_position
        self.velocity = initial_velocity
        self.acceleration = acceleration
        self.radius = 10
        self.width = 2

        self.image = pygame.image.load(IMAGE_PATH).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width*self.radius, self.width*self.radius))

    def update(self, dt):
        # gravity
        self.velocity.y = self.velocity.y + self.acceleration * dt

        self.position = self.position + self.velocity * dt

    def draw(self, screen):
        screen.blit(*self.get_image())
    
    def get_image(self):
        new_rect = self.image.get_rect(center = self.image.get_rect(center = tuple(self.position)).center)

        return (self.image, new_rect)
