from abc import ABC, abstractmethod

import pygame

'''
AbstractObject is an abstract class that represents some abstract object in our system
'''
class AbstractObject(ABC):

    x_position: float
    y_position: float
    height: float
    width: float
    color: pygame.Color
    is_visible: bool

    @abstractmethod
    def __init__(self, x_position: float, y_position: float, height: float, width: float, color: pygame.Color, is_visible=True):
        self.x_position = x_position
        self.y_position = y_position
        self.height = height
        self.width = width
        self.color = color
        self.is_visible = is_visible

    @abstractmethod
    def render(self,screen):
        pass