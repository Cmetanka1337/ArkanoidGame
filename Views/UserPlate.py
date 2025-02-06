from Views.Abstract_classes.AbstractMovableObject import AbstractMovableObject

class UserPlateObject(AbstractMovableObject):

    def __init__(self, x_position: float, y_position: float, width: float, height: float, color: str):
        super().__init__(x_position, y_position, height, width, color, True)

    def render(self):
        pass

    def move_to(self, x: float, y: float):
        pass

    def resize(self, new_width: float):
        pass