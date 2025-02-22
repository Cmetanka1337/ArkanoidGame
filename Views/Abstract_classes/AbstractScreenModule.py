from abc import ABC, abstractmethod
import pygame


class AbstractScreen(ABC):

    def __init__(self, manager, window_surface):
        self.window_surface = window_surface
        self.manager = manager
        self.background = pygame.Surface(window_surface.get_size())
        self.background.fill('LavenderBlush')
        self.window_width, self.window_height = window_surface.get_size()

    @abstractmethod
    def process_events(self, event):
        pass

    def draw(self):
        self.window_surface.blit(self.background, (0, 0))
        self.manager.draw_ui(self.window_surface)