from abc import ABC, abstractmethod

from Views.Abstract_classes import AbstractObject
from Views.Abstract_classes.AbstractMovableObject import AbstractMovableObject
import pygame


'''
AbstractBonusObject its a basic abstract class that represents bonuses in our system
'''
class AbstractBonusObject(AbstractMovableObject):
    speed: float
    move_direction = [0,1]
    radius: float
    is_active: bool
    @abstractmethod
    def __init__(self, x_position: float, y_position: float, height: float, width: float, color: pygame.Color,
                 is_visible,speed: float, move_direction: list, radius: float, is_active: bool):
        super().__init__(x_position, y_position, height, width, color, is_visible)
        self.speed = speed
        self.move_direction = move_direction
        self.radius = radius
        self.is_active = is_active

    def move_to(self, x: float, y: float):
        # встановлюємо напрямок руху а потім рухаємо в тому напрямку мяч бонусу змінюючи координати х та у
        self.move_direction[0] = x
        self.move_direction[1] = y
        self.x_position += self.speed * self.move_direction[0]
        self.y_position += self.speed * self.move_direction[1]

    def update_position(self):
        """
        Оновлює позицію м'яча згідно з поточним напрямком руху та швидкістю.
        """
        self.x_position += self.speed * self.move_direction[0]
        self.y_position += self.speed * self.move_direction[1]

    def render(self,screen):
        pygame.draw.circle(screen, self.color,(int(self.x_position), int(self.y_position)),int(self.radius))
    #condition for activation bonus
    def calculate_reflection(self,user_plate,game_screen :"GameScreen"):
        if not self.is_active and self.is_visible and self.move_direction[1] > 0:
            # Перевірка, чи досяг мяч верхньої межі платформи
            if self.y_position + self.radius >= user_plate.rect.y:
                # Перевірка, чи знаходиться мяч по осі X в межах платформи
                if user_plate.rect.x <= self.x_position <= user_plate.rect.x + user_plate.rect.width:
                    # Модель бонусу зникає та активується сам бонус
                    self.is_visible = False
                    self.is_active = True
                    self.activate(game_screen)
    #abstract methods for activating and deactivating bonuses
    @abstractmethod
    def activate(self, target: AbstractObject):
        pass

    @abstractmethod
    def deactivate(self, target: AbstractObject):
        pass
