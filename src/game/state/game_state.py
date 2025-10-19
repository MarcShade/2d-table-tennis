import pygame

from src.game.state.state import State
from src.game.ball import Ball
from src.game.paddle import Paddle

from src.utils.math.vector import Vector2
from src.utils.handlers.text_handler import TextHandler

from random import randint
from time import time, sleep

BACKGROUND_PATH = "assets/textures/background.jpg"
RED_PADDLE_PATH = "assets/textures/redbat.png"
BLACK_PADDLE_PATH = "assets/textures/blackbat.png"
TABLE_PATH = "assets/textures/table.png"

WHITE = (255, 255, 255)

class GameState(State):
    def __init__(self, engine):
        super().__init__(engine)
        self.acceleration = 9.82
        self.ball = Ball(Vector2(500, 500), Vector2(100, 1), self.acceleration)
        
        self.paddles = [Paddle(100, 600, RED_PADDLE_PATH, 1, self.engine), Paddle(1500, 600, BLACK_PADDLE_PATH, 2, self.engine)]
        self.background = pygame.image.load(BACKGROUND_PATH).convert()
        self.table_image = pygame.image.load(TABLE_PATH).convert_alpha()
        self.table_image = pygame.transform.scale(self.table_image, (1000, 500))

        self.last_hit = None
        self.hit_table = False
        self.points = [0, 0]

        self.new_rally(0)
    
    def update(self, fr):
        for paddle in self.paddles:
            paddle.update(fr)
        self.ball.update(fr)
        self.update_collision()
        self.validate_play()

    def paddle_collision(self, paddle):
        self.ball.velocity = self.paddles[paddle].compute_normal() * self.ball.velocity.length() * self.paddles[paddle].outgoing_velocity
        pygame.mixer.Sound(f"assets/sounds/paddlehit1.mp3").play()
        self.last_hit = paddle
        self.hit_table = False
        self.ball.table_hits = 0

        self.paddles[paddle].outgoing_velocity = 0.5

    def update_collision(self):       
        if self.paddles[0].compute_dist_from_ball(self.ball.position) < 10 and self.paddles[0].compute_center_dist(self.ball.position) < 75 and self.ball.velocity.x <= 0:
            self.paddle_collision(0)

        if self.paddles[1].compute_dist_from_ball(self.ball.position) < 10 and self.paddles[1].compute_center_dist(self.ball.position) < 75 and self.ball.velocity.x >= 0:
            self.paddle_collision(1)

        if (self.ball.position.y > 675 and self.ball.velocity.y == abs(self.ball.velocity.y)):
            if self.ball.position.x > 300 and self.ball.position.x < 1300:
                self.ball.table_hits += 1
                self.ball.velocity.y *= -1
                pygame.mixer.Sound(f"assets/sounds/tablehit{randint(1,2)}.mp3").play()
            # Oh no! I missed the table
    
    def validate_play(self):
        if (self.ball.position.y + self.ball.radius) > 900:
            if self.hit_table:
                self.points[self.last_hit] += 1
                self.new_rally(self.last_hit)
            else:
                self.points[(self.last_hit + 1) % 2] += 1
                self.new_rally((self.last_hit + 1) % 2)
            return

        if (self.ball.position.x - self.ball.radius) < 0 or (self.ball.position.x + self.ball.radius) > 1600:
            if self.hit_table:
                self.points[self.last_hit] += 1
                self.new_rally(self.last_hit)
            else:
                self.points[(self.last_hit + 1) % 2] += 1
                self.new_rally((self.last_hit + 1) % 2)
            return
        
        if self.ball.table_hits > 2:
            not_hit = (self.last_hit + 1) % 2
            self.points[not_hit] += 1
            self.ball.table_hits = 0
            self.new_rally(not_hit)

        if self.points[0] == 11 or self.points[1] == 11:
            from src.game.engine import StateEnum
            self.restart()
            self.engine.change_state(StateEnum.End)

    def new_rally(self, serving_player):
        if self.points[0] != 0 or self.points[1] != 0:
            sleep(0.5)
        self.ball.velocity = Vector2(0, -75)
        self.ball.position = Vector2(self.paddles[serving_player].position.x, 400)
        self.paddles[0].reset()
        self.paddles[1].reset()

    def restart(self):
        self.paddles[0].reset()
        self.paddles[1].reset()

        self.last_hit = None
        self.hit_table = False
        self.points = [0, 0]

        self.new_rally(0)

    def render(self, screen):
        screen.blit(self.background, (0, 0))
        screen.blit(self.table_image, self.table_image.get_rect(center = self.table_image.get_rect(center = [800, 775]).center))
        self.ball.draw(screen)
        for paddle in self.paddles:
            paddle.draw(screen)

        TextHandler(self.points[0], screen, Vector2(self.engine.window_size[0]/2 - 300, 100), self.engine.font).render()
        TextHandler(self.points[1], screen, Vector2(self.engine.window_size[0]/2 + 300, 100), self.engine.font).render()

    def handle_input(self, key_set, events):
        for paddle in self.paddles:
            paddle.handle_input(key_set)

        if pygame.K_SPACE in key_set:
            self.paddle_hit(0)
        
        if pygame.K_RSHIFT in key_set:
            self.paddle_hit(1)

        if pygame.K_r in key_set:
                from src.game.engine import StateEnum
                self.restart()
                self.engine.change_state(StateEnum.Menu)
    
    def paddle_hit(self, paddle): # Probably shouldn't be done here
        if (time() - self.paddles[paddle].time_since_last_hit) > self.paddles[paddle].delay:
            self.paddles[paddle].animate()

            self.paddles[paddle].time_since_last_hit = time()
            dist = self.paddles[paddle].compute_dist_from_ball(self.ball.position)

            if dist < 70 and self.paddles[paddle].compute_center_dist(self.ball.position) < 75: 
                outgoing = (70 - dist) / 60 * 2
                outgoing = max(min(outgoing, 3), 0.5) # Clamp the value, because Python provides no way of doing it automatically :(
                self.paddles[paddle].outgoing_velocity = outgoing 
                self.paddles[paddle].animate()
                self.paddle_collision(paddle)