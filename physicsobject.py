class PhysicsObject:
    position: tuple
    velocity: tuple
    acceleration: tuple

    def __init__(self, p: tuple, v: tuple, a: tuple):
        self.position = p
        self.velocity = v
        self.acceleration = a # No need for this to be a tuple since i wont be changing acceleration in the x-direction
