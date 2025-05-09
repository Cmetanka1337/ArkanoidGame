from abc import ABC, abstractmethod

import pygame

from Views.Abstract_classes.AbstractObject import AbstractObject

'''
AbstractStaticObject is an abstract class that represents abstract some movable object in our system
'''
class AbstractMovableObject(AbstractObject):

    @abstractmethod
    def __init__(self, x_position: float, y_position: float, height: float, width: float, color: pygame.Color, is_visible=True):
        super().__init__(x_position, y_position, height, width, color, is_visible)