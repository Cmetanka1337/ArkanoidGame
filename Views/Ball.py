from Views.Abstract_classes.AbstractMovableObject import AbstractMovableObject

class BallObject(AbstractMovableObject):

    speed: float
    move_direction: (int, int)

    def __init__(self, x_position: float, y_position: float,
                 height: float, width: float,
                 color: str,
                 speed: float, move_direction: (int, int)):
        super().__init__(x_position, y_position, height, width, color, True)
        self.speed = speed
        self.move_direction = move_direction

    def render(self):
        pass

    def move_to(self, x: float, y: float):
        pass

