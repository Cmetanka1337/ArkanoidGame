import os
import pygame_gui
import pygame
from pygame_gui import UIManager, UI_BUTTON_PRESSED

class MenuScreen:

    def __init__(self, manager, window_surface):
        self.background = pygame.Surface(window_surface.get_size())
        self.background.fill('LavenderBlush')

        label_rect = pygame.Rect(0, 100, 250, 50)
        label_rect.centerx = window_surface.get_width() // 2
        self.label = pygame_gui.elements.UILabel(
            relative_rect=label_rect,
            text="Arkanoid Game",
            manager=manager
        )

        start_button_rect = pygame.Rect(0, label_rect.bottom + 10, 200, 50)
        start_button_rect.centerx = window_surface.get_width() // 2
        self.start_button = pygame_gui.elements.UIButton(
            relative_rect=start_button_rect,
            text="Start Game",
            manager=manager
        )

        settings_button_rect = pygame.Rect(0, start_button_rect.bottom + 10, 200, 50)
        settings_button_rect.centerx = window_surface.get_width() // 2
        self.settings_button = pygame_gui.elements.UIButton(
            relative_rect=settings_button_rect,
            text="Settings",
            manager=manager
        )

    def process_events(self, event):
            """ Обробка натискань кнопок """
            if event.type == UI_BUTTON_PRESSED:
                if event.ui_element == self.start_button:
                    return "game"
                elif event.ui_element == self.settings_button:
                    return "settings"
            return None

    def draw(self, manager, window_surface):
        """ Малюємо меню на екрані """
        window_surface.blit(self.background, (0, 0))
        manager.draw_ui(window_surface)