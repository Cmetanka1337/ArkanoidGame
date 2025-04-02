from Models.LocalizedStrings import LocalizedStrings


class LocalizedStringEnglish(LocalizedStrings):
    localized_strings_name = "English"

    def __init__(self):
        self.game_name_str = "Arkanoid Game"
        self.start_game_str = "Start game"
        self.settings_str = "Settings"
        self.background_str = "Background"
        self.language_str = "Language"
        self.music_str = "Music"
        self.start_str = "Start"
        self.back_str = "Back"
        self.game_is_paused_str = "Game is paused"
        self.return_str = "Return"
        self.back_to_menu_str = "Back to menu"
        self.save_str = "Save"
        self.choose_level_str = "Choose level"
        self.level_completed_str = "Level completed"
        self.next_level_str = "Next level"
        self.restart_str = "Restart"
        self.game_over_str = "Game over"

        super().__init__(self.localized_strings_name, self.game_name_str, self.start_game_str, self.settings_str, self.background_str, self.language_str, self.music_str, self.start_str, self.back_str,
                         self.game_is_paused_str, self.return_str, self.back_to_menu_str, self.save_str, self.choose_level_str, self.next_level_str, self.level_completed_str, self.restart_str, self.game_over_str)

    def return_new_instance(self):
        return self