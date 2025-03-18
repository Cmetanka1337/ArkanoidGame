from Models.LocalizedStrings import LocalizedStrings


class LocalizedStringEnglish(LocalizedStrings):
    def __init__(self):

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

        super().__init__(self.start_game_str, self.settings_str, self.background_str, self.language_str, self.music_str, self.start_str, self.back_str,
                         self.game_is_paused_str, self.return_str, self.back_to_menu_str, self.save_str)