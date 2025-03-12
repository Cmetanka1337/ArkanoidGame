from Views.Abstract_classes import AbstractObject
from Views.Abstract_classes.AbstractBonusObject import AbstractBonusObject
import pygame

from Views.Ball import BallObject


'''
AdditionalBallsBonus its implementation of AbstractBonusObject for additional balls bonus
'''
class AdditionalBallsBonus(AbstractBonusObject):
    balls_number:float
    def __init__(self, x_position: float, y_position: float,
                 height: float, width: float,
                 color: pygame.Color, speed: float, move_direction: list, radius: float,
                 is_active: bool, balls_number: float):
        super().__init__(x_position, y_position, height, width, color, True,speed,move_direction,radius,is_active)
        self.balls_number = balls_number
    #adds balls to screen and activates bonus
    def activate(self, target: "GameScreen"):
        print("Активовано бонус, balls_number =", self.balls_number)
        base_x, base_y = 200, 100  # або позиція вже існуючого м'яча
        for i in range(int(self.balls_number)):
            new_x = base_x + i * 20  # зсув по горизонталі
            new_y = base_y  # або додатковий зсув по вертикалі
            target.balls.append(BallObject(new_x, new_y, 10, 10, pygame.Color(255, 0, 0), 5, [1, 1], 5, True))
        self.is_active = True


    def deactivate(self, target: AbstractObject):
        pass

