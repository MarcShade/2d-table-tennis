from src.utils.math.vector import Vector2
from src.game.engine import GameEngine


class TextHandler:
    def __init__(self, text, screen, position: Vector2, font):
        self.text = str(text)
        self.screen = screen
        self.position = position
        self.font = font

    def render(self):
        text = self.font.render(self.text, 1, (0,0,0))
        text_rect = text.get_rect(center=(self.position.x, self.position.y))
        self.screen.blit(text, text_rect)