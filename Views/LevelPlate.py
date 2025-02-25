import pygame
from Models.Bonus import BonusObject
from Views.Abstract_classes.AbstractStaticObject import AbstractStaticObject

class LevelPlateObject(AbstractStaticObject):

    hit_points: int
    plate_type: str # standard plate or with a bonus, for example
    alpha:int
    def __init__(self,hit_points: int, plate_type: str, is_breakable: bool, x_position: float, y_position: float, height: float, width: float,
                 color: pygame.Color, is_visible=True):
        super().__init__(is_breakable, x_position, y_position, height, width, color, is_visible)
        self.hit_points = hit_points
        self.plate_type = plate_type
        self.alpha = 255
        self.rect = pygame.Rect(x_position, y_position, width, height)
        self.color.a = self.alpha
    def render(self, screen):
        """ Малює платформу, якщо вона видима """
        if self.is_visible:
         pygame.draw.rect(screen, self.color, self.rect)


    def decrease_hit_points(self):
        """ Зменшує міцність платформи, робить її невидимою при руйнуванні """
        if self.is_breakable:
            self.hit_points -= 1
            if self.hit_points > 0:
                alpha_values = {3: 255, 2: 170, 1: 85}
                self.alpha = alpha_values.get(self.hit_points,50)
                self.color.a = self.alpha
            else:
                self.is_visible = False


    def spawn_bonus(self) -> BonusObject:
        pass

    def update_state(self):
        pass