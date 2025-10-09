import pygame

from src.game.state.state import State

from src.utils.math.vector import Vector2
from src.utils.handlers.text_handler import TextHandler

class EndState(State):
    def __init__(self, engine):
        super().__init__(engine)
        self.engine = engine

        button_size = Vector2(350, 180)
        screen_center = Vector2(
            engine.window_size[0] // 2, engine.window_size[1] // 2
        )

        self.restart_button = pygame.Rect(
            int(screen_center.x - button_size.x / 2),
            int(screen_center.y - button_size.y / 2),
            int(button_size.x),
            int(button_size.y),
        )

        self.restart_text = TextHandler("Restart", engine.surface, screen_center, self.engine.font)

    def render(self, surface):
        surface.fill((255, 255, 255))

        pygame.draw.rect(surface, (0, 200, 0), self.restart_button, border_radius=20)

        self.restart_text.render()

    def handle_input(self, keys, events):
        from src.game.engine import StateEnum
        if pygame.K_RETURN in keys:
            self.engine.change_state(StateEnum.Menu)

        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                if self.restart_button.collidepoint(pygame.mouse.get_pos()):
                    self.engine.change_state(StateEnum.Menu)