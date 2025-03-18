from Models.LocalizedStringEnglish import LocalizedStringEnglish
from Models.LocalizedStrings import LocalizedStrings


class LocalizedStringUkrainian(LocalizedStrings):
    localized_strings_name = "Українська"

    def __init__(self):

        self.game_name_str = "Арканоїд"
        self.start_game_str = "Почати гру"
        self.settings_str = "Налаштування"
        self.background_str = "Фон"
        self.language_str = "Мова"
        self.music_str = "Музика"
        self.start_str = "Почати"
        self.back_str = "Назад"
        self.game_is_paused_str = "Гра на паузі"
        self.return_str = "Відновити гру"
        self.back_to_menu_str = "В меню"
        self.save_str = "Зберегти"
        self.choose_level_str = "Виберіть рівень"
        self.level_completed_str = "Рівень пройдено"
        self.next_level_str = "Наступний рівень"
        self.restart_str = "Перезапустити"

        super().__init__(self.localized_strings_name, self.game_name_str, self.start_game_str, self.settings_str, self.background_str, self.language_str, self.music_str, self.start_str, self.back_str,
                         self.game_is_paused_str, self.return_str, self.back_to_menu_str, self.save_str, self.choose_level_str, self.next_level_str, self.level_completed_str, self.restart_str)


    def return_new_instance(self):
        return self