from Models.LocalizedStringEnglish import LocalizedStringEnglish
from Models.LocalizedStrings import LocalizedStrings


class LocalizedStringUkrainian(LocalizedStrings):
    def __init__(self):

        self.start_game_str = "Почати гру"
        self.settings_str = "Налаштування"
        self.background_str = "Фон"
        self.language_str = "Мова"
        self.music_str = "Музика"
        self.start_str = "Почати"
        self.back_str = "Назад"
        self.game_is_paused_str = "Гра на паузі"
        self.return_str = "Повернутися"
        self.back_to_menu_str = "Повернутися до меню"
        self.save_str = "Зберегти"

        super().__init__(self.start_game_str, self.settings_str, self.background_str, self.language_str, self.music_str, self.start_str, self.back_str,
                         self.game_is_paused_str, self.return_str, self.back_to_menu_str, self.save_str)