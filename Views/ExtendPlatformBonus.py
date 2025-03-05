from Views.Abstract_classes import AbstractObject
from Views.Abstract_classes.AbstractBonusObject import AbstractBonusObject
import pygame


from Views.UserPlate import UserPlateObject

class ExtendPlatformBonus(AbstractBonusObject):
    duration:float
    extend_size:float
    def __init__(self, x_position: float, y_position: float,
                 height: float, width: float,
                 color: pygame.Color, speed: float, move_direction: list, radius: float,
                 is_active: bool, duration: float,extend_size: float):
        super().__init__(x_position, y_position, height, width, color, True,speed,move_direction,radius,is_active)
        self.duration = duration
        self.extend_size = extend_size
        self.start_time = None

    def activate(self, target: "UserPlateObject"):
        self.start_time = pygame.time.get_ticks()
        self.is_active = True
        self.start_time = pygame.time.get_ticks()
        target.resize(self.extend_size)

    def deactivate(self, target: "UserPlateObject"):
        self.is_active = False

    def update(self, target: "UserPlateObject"):
        if self.is_active:
            current_time = pygame.time.get_ticks()
            elapsed_time = (current_time - self.start_time) / 1000.0  # секунди
            if elapsed_time >= self.duration:
                target.resize(200)  # повертаємо до стандартного розміру
                self.deactivate(target)

