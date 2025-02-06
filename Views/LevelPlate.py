from Models.Bonus import BonusObject
from Views.Abstract_classes.AbstractStaticObject import AbstractStaticObject

class LevelPlateObject(AbstractStaticObject):

    hit_points: int
    plate_type: str # standard plate or with a bonus, for example

    def __init__(self,hit_points: int, plate_type: str, is_breakable: bool, x_position: float, y_position: float, height: float, width: float,
                 color: str, is_visible=True):
        super().__init__(is_breakable, x_position, y_position, height, width, color, is_visible)
        self.hit_points = hit_points
        self.plate_type = plate_type

    def render(self):
        pass

    def decrease_hit_points(self):
        pass

    def spawn_bonus(self) -> BonusObject:
        pass

    def update_state(self):
        pass