import pygame_gui
import pygame
from pygame_gui import UI_BUTTON_PRESSED
from Views.Abstract_classes.AbstractScreenModule import AbstractScreen

class MenuScreen(AbstractScreen):

    def __init__(self, manager, window_surface):
        super().__init__(manager, window_surface)
        self.layout_elements()


    def process_events(self, event):
            """ Обробка натискань кнопок """
            if event.type == UI_BUTTON_PRESSED:
                if event.ui_element == self.start_button:
                    return "lvl_selection"
                elif event.ui_element == self.settings_button:
                    return "settings"
            return None

    def layout_elements(self):
        from Controllers import GameModule
        label_rect = pygame.Rect(0, 100, 250, 50)
        label_rect.centerx = self.window_surface.get_width() // 2
        self.label = pygame_gui.elements.UILabel(
            relative_rect=label_rect,
            text=GameModule.selected_language.game_name_str,
            manager=self.manager
        )

        start_button_rect = pygame.Rect(0, label_rect.bottom + 10, 200, 50)
        start_button_rect.centerx = self.window_surface.get_width() // 2
        self.start_button = pygame_gui.elements.UIButton(
            relative_rect=start_button_rect,
            text=GameModule.selected_language.start_str,
            manager=self.manager
        )

        settings_button_rect = pygame.Rect(0, start_button_rect.bottom + 10, 200, 50)
        settings_button_rect.centerx = self.window_surface.get_width() // 2
        self.settings_button = pygame_gui.elements.UIButton(
            relative_rect=settings_button_rect,
            text=GameModule.selected_language.settings_str,
            manager=self.manager
        )