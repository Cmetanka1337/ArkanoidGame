from pygame import Rect
from pygame_gui import UI_BUTTON_PRESSED
from pygame_gui.elements import UILabel, UIButton, UIDropDownMenu
import pygame
from Views.Abstract_classes.AbstractScreenModule import AbstractScreen


class LevelSelection(AbstractScreen):
    def __init__(self, manager, window_surface):
        super().__init__(manager, window_surface)

        self.window_width, self.window_height = window_surface.get_size()
        self.selected_level=1
        self.layout_elements()


    def process_events(self, event):
        if event.type == UI_BUTTON_PRESSED and event.ui_element == self.back_button:
            return "menu"
        if event.type == UI_BUTTON_PRESSED and event.ui_element == self.start_button:
            selected_option = self.level_menu.selected_option
            if isinstance(selected_option, tuple):
                selected_option = selected_option[0]
            try:
                selected_level = int(selected_option.split()[-1])
            except ValueError:
                selected_level = 1
            self.selected_level = selected_level
            return "game"
        return None

    def layout_elements(self):
        from Controllers import GameModule
        padding_x = 30
        padding_y = 20
        label_height = 50
        control_width = 200
        button_width = 150
        button_height = 50

        title_rect = Rect((self.window_width // 2 - 100, 20), (200, 70))
        self.title_label = UILabel(
            relative_rect=title_rect,
            text=GameModule.selected_language.choose_level_str,
            manager=self.manager
        )

        level_menu_rect = Rect(title_rect.x, title_rect.y + padding_y * 4, control_width, label_height)
        self.level_menu = UIDropDownMenu(
            relative_rect=level_menu_rect,
            options_list=["Level 1","Level 2"],
            manager=self.manager,
            starting_option="Level 1"
        )

        start_button_rect = Rect(level_menu_rect.x + padding_x, level_menu_rect.y + padding_y * 5, button_width, button_height)
        self.start_button = UIButton(
            relative_rect=start_button_rect,
            text=GameModule.selected_language.start_str,
            manager=self.manager
        )

        back_button_rect = Rect(start_button_rect.x, start_button_rect.y + padding_y * 3, button_width, button_height)
        self.back_button = UIButton(
            relative_rect=back_button_rect,
            text=GameModule.selected_language.back_str,
            manager=self.manager
        )

