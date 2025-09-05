class PhysicsObject:
    position: list
    velocity: list
    acceleration: int

    def __init__(self, p: list, v: list, a: list):
        self.position = p
        self.velocity = v
        self.acceleration = a
