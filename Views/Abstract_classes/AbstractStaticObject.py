from abc import ABC, abstractmethod
from Views.Abstract_classes.AbstractObject import AbstractObject
import pygame
'''
AbstractStaticObject is an abstract class that represents abstract some static object in our system
'''
class AbstractStaticObject(AbstractObject):

    is_breakable: bool

    @abstractmethod
    def __init__(self, is_breakable: bool , x_position: float, y_position: float, height: float, width: float, color: pygame.Color, is_visible=True):
        super().__init__(x_position, y_position, height, width, color, is_visible)
        self.is_breakable = is_breakable