import pygame
from src.utils.math.vector import Vector2
from src.utils.handlers.text_handler import TextHandler

class MenuState:
    def __init__(self, engine):
        super().__init__()
        self.engine = engine

        button_size = Vector2(300, 120)
        screen_center = Vector2(
            engine.window_size[0] // 2, engine.window_size[1] // 2
        )

        self.play_button = pygame.Rect(
            int(screen_center.x - button_size.x / 2),
            int(screen_center.y - button_size.y / 2),
            int(button_size.x),
            int(button_size.y),
        )

        self.play_text = TextHandler("PLAY", engine.surface, screen_center, self.engine.font)

    def enter(self):
        pass

    def exit(self):
        pass

    def update(self, dt):
        pass

    def render(self, surface):
        surface.fill((255, 255, 255))

        pygame.draw.rect(surface, (0, 200, 0), self.play_button, border_radius=20)

        self.play_text.render()

    def handle_input(self, keys):
        if pygame.K_RETURN in keys:
            self.engine.change_state("game")

        mouse_pressed = pygame.mouse.get_pressed()
        if mouse_pressed[0]:
            if self.play_button.collidepoint(pygame.mouse.get_pos()):
                self.engine.change_state("game")
