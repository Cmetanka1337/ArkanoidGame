from pygame import Rect
from pygame_gui import UI_BUTTON_PRESSED, UIManager, UI_DROP_DOWN_MENU_CHANGED, UI_HORIZONTAL_SLIDER_MOVED
from pygame_gui.elements import UILabel, UIButton, UIHorizontalSlider, UIDropDownMenu
from Models.LocalizedStringEnglish import LocalizedStringEnglish
from Models.LocalizedStringUkrainian import LocalizedStringUkrainian
from Views.Abstract_classes.AbstractScreenModule import AbstractScreen


class SettingsScreen(AbstractScreen):
    manager: UIManager

    def __init__(self, manager, window_surface, settings_controller):
        super().__init__(manager, window_surface)


        self.language_map = {
            LocalizedStringEnglish.localized_strings_name: LocalizedStringEnglish(),
            LocalizedStringUkrainian.localized_strings_name: LocalizedStringUkrainian()
        }

        self.background_color_map = {
            "Blue": "blue_theme.json",
            "Purple" : "purple_theme.json",
            "Yellow" : "yellow_theme.json"
        }
        self.background_keys_list = list(self.background_color_map.keys())

        game_module_background_str = settings_controller.get_background()
        self.current_background = next(
            (key for key, value in self.background_color_map.items() if value == game_module_background_str),
            "Blue"
        )

        self.settings_controller = settings_controller
        self.window_width, self.window_height = window_surface.get_size()
        self.layout_elements()

    def process_events(self, event):
        if event.type == UI_BUTTON_PRESSED and event.ui_element == self.back_button:
            return "menu"
        elif event.type == UI_HORIZONTAL_SLIDER_MOVED and event.ui_element == self.music_level_slider:
            self.settings_controller.change_volume(self.music_level_slider.get_current_value())

        elif event.type == UI_DROP_DOWN_MENU_CHANGED and event.ui_element == self.background_color_menu:
            selected_theme = self.background_color_map.get(self.background_color_menu.selected_option[0])
            if selected_theme:
                self.settings_controller.change_background(selected_theme)

        elif event.type == UI_DROP_DOWN_MENU_CHANGED and event.ui_element == self.language_menu:
            selected_language = self.language_map.get(self.language_menu.selected_option[0])
            if selected_language:
                self.settings_controller.change_language(selected_language)

        return None

    def layout_elements(self):

        from Controllers import GameModule
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
            text=GameModule.selected_language.settings_str,
            manager=self.manager
        )


        background_label_rect = Rect(padding_x, title_rect.bottom + padding_y, label_width, label_height)
        self.background_label = UILabel(
            relative_rect=background_label_rect,
            text=GameModule.selected_language.background_str,
            manager=self.manager
        )

        background_color_menu_rect = Rect(control_x, background_label_rect.y, control_width, label_height)
        self.background_color_menu = UIDropDownMenu(
            relative_rect=background_color_menu_rect,
            options_list=self.background_keys_list ,
            manager=self.manager,
            starting_option=self.current_background
        )

        language_label_rect = Rect(padding_x, background_label_rect.bottom + padding_y, label_width, label_height)
        self.language_label = UILabel(
            relative_rect=language_label_rect,
            text=GameModule.selected_language.language_str,
            manager=self.manager
        )

        language_menu_rect = Rect(control_x, language_label_rect.y, control_width, label_height)
        self.language_menu = UIDropDownMenu(
            relative_rect=language_menu_rect,
            options_list=[LocalizedStringEnglish.localized_strings_name, LocalizedStringUkrainian.localized_strings_name],
            manager=self.manager,
            starting_option=GameModule.selected_language.localized_strings_name
        )

        music_level_label_rect = Rect(padding_x, language_label_rect.bottom + padding_y, label_width, label_height)
        self.music_level_label = UILabel(
            relative_rect=music_level_label_rect,
            text=GameModule.selected_language.music_str,
            manager=self.manager
        )

        music_level_slider_rect = Rect(control_x, music_level_label_rect.centery - 10, slider_width, 20)
        self.music_level_slider = UIHorizontalSlider(
            relative_rect=music_level_slider_rect,
            start_value=self.settings_controller.get_volume(),
            value_range=(0, 1),
            manager=self.manager
        )

        back_button_rect = Rect(control_x, self.window_height - button_height - padding_y, button_width, button_height)
        self.back_button = UIButton(
            relative_rect=back_button_rect,
            text=GameModule.selected_language.back_str,
            manager=self.manager
        )