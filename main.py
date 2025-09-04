import pygame
from pygame.locals import *
from engine import Engine

engine = Engine(60, (800, 450))

pygame.init()
surface = pygame.display.set_mode((1600, 900))
pygame.display.set_caption('GeeksforGeeks')

running = True

while running:
    surface.fill((0, 0, 0, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    engine.update()
    pygame.draw.circle(surface, (255, 255, 255, 255), engine.ball.position, 10)
    pygame.draw.rect(surface, (255, 255, 255, 255), engine.paddles[0].position, engine.paddles[0].height, engine.paddles[0].width)

    pygame.display.update()

    print(engine.ball.velocity)