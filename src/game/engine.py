import pygame
from pygame.locals import *
import sys

from enum import Enum

class StateEnum(Enum):
    Menu = "menu"
    Game = "game"
    End = "end"
    
class GameEngine:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("2D Table Tennis")
        self.window_size = (1600, 900)
        self.surface = pygame.display.set_mode(self.window_size) 

        self.font = pygame.font.SysFont('Comic Sans MS', 100)

        self.clock = pygame.time.Clock()
        self.running = True

        self.state = None
        self.state_classes = {}
        self.state_cache = {}

        # self.FPS = 144
        self.key_set = set()

    def register_states(self):
        from src.game.state.menu_state import MenuState
        from src.game.state.game_state import GameState
        from src.game.state.end_state import EndState

        self.state_classes = {
            StateEnum.Menu: MenuState,
            StateEnum.Game: GameState,
            StateEnum.End: EndState
            }

    def run(self, initial_state):
        self.register_states()
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
        if new_state not in self.state_cache:
            state_class = self.state_classes[new_state]
            self.state_cache[new_state] = state_class(self)

        self.state = self.state_cache[new_state]
        self.state.enter()

    def handle_input(self, events):
        for event in events:
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.quit()
            if event.type == pygame.KEYDOWN:
                self.key_set.add(event.key)
            elif event.type == pygame.KEYUP:
                self.key_set.discard(event.key)
        self.state.handle_input(self.key_set, events)