import pygame
from pygame.locals import *
from engine import GameEngine
from vector import Vector2

FRAMERATE = 60 # cap framerate using time lib later maybe idk

pygame.init()
surface = pygame.display.set_mode((1600, 900))
pygame.display.set_caption("2D Ping Pong")

engine = GameEngine(FRAMERATE, Vector2(800, 450), surface)
background = pygame.image.load("./Assets/Images/background.jpg").convert()
running = True

while running:
    surface.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            engine.key_set.add(event.key)
        elif event.type == pygame.KEYUP:
            engine.key_set.discard(event.key)   

    engine.update()
    pygame.display.update()