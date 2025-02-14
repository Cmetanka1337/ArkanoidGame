import pygame
import pygame_gui
from pygame_gui import UI_BUTTON_PRESSED

class GameScreen:

    def __init__(self, manager, window_surface):
        self.background = pygame.Surface(window_surface.get_size())
        self.background.fill('LightBlue')


        back_button_rect = pygame.Rect(20, 20, 150, 50)
        self.back_button = pygame_gui.elements.UIButton(
            relative_rect=back_button_rect,
            text="Back to Menu",
            manager=manager
        )

    def process_events(self, event):
        if event.type == UI_BUTTON_PRESSED and event.ui_element == self.back_button:
            return "menu"
        return None

    def draw(self, manager, window_surface):
        window_surface.blit(self.background, (0, 0))
        manager.draw_ui(window_surface)