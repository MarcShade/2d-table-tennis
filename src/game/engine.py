import pygame
from pygame.locals import *
import sys

from src.game.state.menu_state import MenuState
from src.game.state.game_state import GameState

class GameEngine:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("2D настольный теннис")
        self.window_size = (1600, 900)
        self.surface = pygame.display.set_mode(self.window_size) 
        self.font = pygame.font.SysFont('Comic Sans MS', 100)
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = None
        # self.FPS = 144
        self.key_set = set()

        self.state_classes = {
            "menu": MenuState,
            "game": GameState,
        }

    def run(self, initial_state):
        self.change_state(initial_state)
        while self.running:
            fr = 1/60
            events = pygame.event.get()
            self.handle_input(events)
            self.state.update(fr)
            self.state.render(self.surface)
            pygame.display.flip()
        pygame.quit()
        sys.exit()
    
    def quit(self):
        self.running = False

    def change_state(self, new_state):
        if self.state != None:
            self.state.exit()
        if new_state not in self.state_classes:
            raise ValueError(f"Unknown state: {new_state}")

        self.state = self.state_classes[new_state](self)
        self.state.enter()

    def handle_input(self, events):
        for event in events:
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.quit()
            if event.type == pygame.KEYDOWN:
                self.key_set.add(event.key)
            elif event.type == pygame.KEYUP:
                self.key_set.discard(event.key)
        self.state.handle_input(self.key_set)