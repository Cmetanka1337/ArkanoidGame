import pygame
from Views.Abstract_classes.AbstractMovableObject import AbstractMovableObject
from Views.Scene import SceneObject
class UserPlateObject(AbstractMovableObject):

    def __init__(self, x_position: float, y_position: float, width: float, height: float, color: pygame.Color, speed: float):
        super().__init__(x_position, y_position, height, width, color, True)
        self.scene_width =SceneObject.width
        self.speed = speed
        self.rect=pygame.Rect(x_position, y_position, width, height)

    def render(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def move_to(self, x: float, y: float):
        if 0<=x<self.scene_width - self.rect.width:
            self.rect.x=x
        else:
            self.rect.x = max(0, min(x, self.scene_width - self.rect.width))
        self.rect.y=y

    def resize(self, new_width: float):
        self.rect.width=new_width
        if self.rect.right>self.scene_width:
            self.rect.x=self.scene_width-self.rect.width



