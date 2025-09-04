from physicsobject import PhysicsObject
from paddle import Paddle

class Engine:
    def __init__(self, fr: int, position: tuple):
        self.ball = PhysicsObject(position, (100, 1), (0, 10))
        self.dt = 1/fr
        self.paddles = [Paddle(30, 30)]


    def update(self):
        self.update_position()
        self.update_collision()

    def update_position(self):
        dv_x = self.ball.velocity[0] + self.ball.acceleration[0] * self.dt
        dv_y = self.ball.velocity[1] + self.ball.acceleration[1] * self.dt

        self.ball.velocity = (dv_x, dv_y)

        dx = self.ball.position[0] + self.ball.velocity[0] * self.dt
        dy = self.ball.position[1] + self.ball.velocity[1] * self.dt

        self.ball.position = (dx, dy)
    
    def update_collision(self):
        if self.ball.position[1] > 900:
            x = self.ball.velocity[0]
            y = -self.ball.velocity[1]
            self.ball.velocity = (x, y)

        if self.ball.position[0] < 0 or self.ball.position[0] > 1600:
            x = -self.ball.velocity[0]
            y = self.ball.velocity[1]
            self.ball.velocity = (x, y)

