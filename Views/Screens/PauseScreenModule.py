import pygame
from pygame import Rect
from pygame_gui import UI_BUTTON_PRESSED
from pygame_gui.elements import UIButton, UILabel
from Views.Abstract_classes.AbstractScreenModule import AbstractScreen


class PauseScreen(AbstractScreen):
    def __init__(self, window_surface, manager):
        super().__init__(manager, window_surface)
        self.manager = manager
        self.elements = []
        self.layout_elements()

    def layout_elements(self):
        from Controllers import GameModule
        """Розташування елементів UI на екрані паузи."""

        title_rect = Rect((self.window_width // 2 - 120, 100), (250, 100))
        self.title_label = UILabel(
            relative_rect=title_rect,
            text=GameModule.selected_language.game_is_paused_str,
            manager=self.manager
        )
        self.elements.append(self.title_label)

        return_button_rect = Rect(title_rect.x + 50, title_rect.y + 120, 150, 50)
        self.return_button = UIButton(
            relative_rect=return_button_rect,
            text=GameModule.selected_language.return_str,
            manager=self.manager
        )
        self.elements.append(self.return_button)

        back_button_rect = Rect(return_button_rect.x, return_button_rect.y + 60, 150, 50)
        self.back_button = UIButton(
            relative_rect=back_button_rect,
            text=GameModule.selected_language.back_to_menu_str,
            manager=self.manager
        )
        self.elements.append(self.back_button)

    def draw(self):
        overlay = pygame.Surface(self.window_surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 50))
        self.window_surface.blit(overlay, (0, 0))
        self.manager.draw_ui(self.window_surface)

    def process_events(self, event):
        if event.type == UI_BUTTON_PRESSED:
            if event.ui_element == self.return_button:
                return "game"
            elif event.ui_element == self.back_button:
                self.destroy()
                return "menu"
        return None

    def destroy(self):
        for element in self.elements:
            element.kill()