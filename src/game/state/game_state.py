import pygame

from src.game.state.state import State
from src.game.ball import Ball
from src.game.paddle import Paddle
from src.math.vector import Vector2

from math import cos, sin, atan, pi
from random import randint

BACKGROUND_PATH = "assets/textures/background.jpg"
RED_PADDLE_PATH = "assets/textures/redbat.png"
BLACK_PADDLE_PATH = "assets/textures/blackbat.png"
TABLE_PATH = "assets/textures/table.png"

WHITE = (255, 255, 255)

class GameState(State):
    def __init__(self, engine):
        super().__init__(engine)
        self.acceleration = 5
        self.ball = Ball(Vector2(900, 600), Vector2(100, 1), self.acceleration)
        
        self.paddles = [Paddle(100, 700, RED_PADDLE_PATH, 1), Paddle(1500, 700, BLACK_PADDLE_PATH, 2)]

        self.background = pygame.image.load(BACKGROUND_PATH).convert()
        self.table_image = pygame.image.load(TABLE_PATH).convert_alpha()
        self.table_image = pygame.transform.scale(self.table_image, (1000, 500))
    
    def update(self, fr):
        # self.update_ball_position(fr)
        for paddle in self.paddles:
            paddle.update(fr)
        self.ball.update(fr)
        self.update_collision()

    def update_collision(self):       
        if self.paddles[0].compute_dist_from_ball(self.ball.position) < 10 and self.paddles[0].compute_center_dist(self.ball.position) < 75 and self.ball.velocity.x < 0:
            _beta = atan(1 / -self.paddles[0].a) * 180 / pi
            beta = _beta if _beta < 90 else -180 + _beta
            beta = beta * pi / 180
            
            self.ball.velocity = Vector2(cos(beta), sin(beta)) * self.ball.velocity.length()
            pygame.mixer.Sound(f"assets/sounds/paddlehit1.mp3").play()

        if self.paddles[1].compute_dist_from_ball(self.ball.position) < 10 and self.paddles[1].compute_center_dist(self.ball.position) < 75 and self.ball.velocity.x > 0:
            _beta = atan(1 / -self.paddles[1].a) * 180 / pi
            beta = 180 + _beta if _beta < 90 else 360 - _beta
            beta = beta * pi / 180

            self.ball.velocity = Vector2(cos(beta), sin(beta)) * self.ball.velocity.length()
            pygame.mixer.Sound(f"assets/sounds/paddlehit1.mp3").play()

        if (self.ball.position.y > 675 and self.ball.velocity.y == abs(self.ball.velocity.y)):
            if  self.ball.position.x > 300 and self.ball.position.x < 1300: # Checking if the ball on the table
                self.ball.velocity.y *= -1 # Inverting velocity
                pygame.mixer.Sound(f"assets/sounds/tablehit{randint(1,2)}.mp3").play()
            # Here points should be given to players
    
    def render(self, screen):
        screen.blit(self.background, (0, 0))
        screen.blit(self.table_image, self.table_image.get_rect(center = self.table_image.get_rect(center = [800, 775]).center))
        self.ball.draw(screen)
        for paddle in self.paddles:
            paddle.draw(screen)

    def handle_input(self, key_set):
        for paddle in self.paddles:
            paddle.handle_input(key_set)