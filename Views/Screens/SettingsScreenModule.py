import pygame
import pygame_gui
from pygame import Rect
from pygame_gui import UI_BUTTON_PRESSED, UIManager
from pygame_gui.elements import UILabel, UIButton, UIHorizontalSlider, UIDropDownMenu


class SettingsScreen:
    manager: UIManager

    def __init__(self, manager, window_surface):
        self.background = pygame.Surface(window_surface.get_size())
        self.manager = manager
        self.background.fill('LavenderBlush')

        self.window_width, self.window_height = window_surface.get_size()
        self.layout_elements()

    def process_events(self, event):
        if event.type == UI_BUTTON_PRESSED and event.ui_element == self.back_button:
            return "menu"

        return None

    def draw(self, manager, window_surface):
        window_surface.blit(self.background, (0, 0))
        manager.draw_ui(window_surface)

    def layout_elements(self):
        padding_x = 30
        padding_y = 20
        label_width = 170
        label_height = 50
        control_width = 200
        slider_width = 220
        button_width = 150
        button_height = 50

        control_x = self.window_width - control_width - padding_x

        title_rect = Rect((self.window_width // 2 - 100, 20), (200, 70))
        self.title_label = UILabel(
            relative_rect=title_rect,
            text="Settings",
            manager=self.manager
        )


        background_label_rect = Rect(padding_x, title_rect.bottom + padding_y, label_width, label_height)
        self.background_label = UILabel(
            relative_rect=background_label_rect,
            text='Background color',
            manager=self.manager
        )

        background_color_menu_rect = Rect(control_x, background_label_rect.y, control_width, label_height)
        self.background_color_menu = UIDropDownMenu(
            relative_rect=background_color_menu_rect,
            options_list=["Light", "Dark", "Green"],
            manager=self.manager,
            starting_option="Light"
        )

        language_label_rect = Rect(padding_x, background_label_rect.bottom + padding_y, label_width, label_height)
        self.language_label = UILabel(
            relative_rect=language_label_rect,
            text='Language',
            manager=self.manager
        )

        language_menu_rect = Rect(control_x, language_label_rect.y, control_width, label_height)
        self.language_menu = UIDropDownMenu(
            relative_rect=language_menu_rect,
            options_list=["English", "Ukrainian"],
            manager=self.manager,
            starting_option="English"
        )

        music_level_label_rect = Rect(padding_x, language_label_rect.bottom + padding_y, label_width, label_height)
        self.music_level_label = UILabel(
            relative_rect=music_level_label_rect,
            text='Music',
            manager=self.manager
        )

        music_level_slider_rect = Rect(control_x, music_level_label_rect.centery - 10, slider_width, 20)
        self.music_level_slider = UIHorizontalSlider(
            relative_rect=music_level_slider_rect,
            start_value=0,
            value_range=(0, 5),
            manager=self.manager
        )

        back_button_rect = Rect(control_x, self.window_height - button_height - padding_y, button_width, button_height)
        self.back_button = UIButton(
            relative_rect=back_button_rect,
            text="Back",
            manager=self.manager
        )