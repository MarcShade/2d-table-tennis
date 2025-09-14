from vector import Vector2
import pygame
from pygame.locals import *

IMAGE_PATH = "Assets/Images/ball.png"

class Ball:
    position: Vector2
    velocity: Vector2
    acceleration: int

    def __init__(self, p: Vector2, v: Vector2, a: list, r: float):
        self.position = p
        self.velocity = v
        self.acceleration = a
        self.radius = r

        self.image = pygame.image.load(IMAGE_PATH).convert_alpha()
        self.image = pygame.transform.scale(self.image, (2*r, 2*r)) # The width is a magic number since I will neither be changing it or referencing it
    
    def get_image(self):
        new_rect = self.image.get_rect(center = self.image.get_rect(center = tuple(self.position)).center)

        return (self.image, new_rect)
