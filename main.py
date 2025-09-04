import pygame
from pygame.locals import *
from engine import GameEngine

FRAMERATE = 60 # cap framerate using time lib later maybe idk

pygame.init()
surface = pygame.display.set_mode((1600, 900))
pygame.display.set_caption("2D Ping Pong")

engine = GameEngine(FRAMERATE, [800, 450], surface)

running = True

while running:
    surface.fill((0, 0, 0, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            engine.key_set.add(event.key)
        elif event.type == pygame.KEYUP:
            engine.key_set.discard(event.key)  # discard avoids KeyError

    engine.update()
    pygame.display.update()