
from Views.Abstract_classes.AbstractBonusObject import AbstractBonusObject
import pygame

from Views.Screens.GameScreenModule import GameScreen
from Views.UserPlate import UserPlateObject


class ExtendPlatformBonus(AbstractBonusObject):

    duration: float
    extend_size: float

    def __init__(self, x_position: float, y_position: float,
                 height: float, width: float,
                 color: pygame.Color, speed: float,
                 move_direction: list, radius: float,
                 is_active: bool, duration: float, extend_size: float):
        super().__init__(x_position, y_position, height, width,
                         color, True, speed, move_direction, radius, is_active)
        self.duration = duration  # наприклад, 10 (секунд)
        self.extend_size = extend_size
        self.start_time = None

    def activate(self, target: "UserPlateObject"):
        # встановлюємо час активації один раз
        self.start_time = pygame.time.get_ticks()
        self.is_active = True
        target.resize(self.extend_size)

    def deactivate(self, target: "UserPlateObject"):
        self.is_active = False
        # Повертаємо платформу до стандартного розміру (наприклад, 200)
        target.resize(200)

    def update(self, target: "UserPlateObject"):
        if self.is_active and self.start_time is not None:
            current_time = pygame.time.get_ticks()
            # переведення в секунди
            elapsed_time = (current_time - self.start_time) / 1000.0
            if elapsed_time > self.duration:
                self.deactivate(target)

    def calculate_reflection(self, user_plate, game_screen: "GameScreen"):
        if (not self.is_active and self.is_visible
                and self.move_direction[1] > 0):
            if self.y_position + self.radius >= user_plate.rect.y:
                if (user_plate.rect.x <= self.x_position <=
                        user_plate.rect.x + user_plate.rect.width):
                    self.is_visible = False
                    self.is_active = True
                    self.activate(user_plate)
