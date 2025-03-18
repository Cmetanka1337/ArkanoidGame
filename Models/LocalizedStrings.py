from abc import ABC, abstractmethod

class LocalizedStrings(ABC):

    localized_strings_name = ""
    game_name_str: str
    start_game_str: str
    settings_str: str
    background_str: str
    language_str: str
    music_str: str
    start_str: str
    back_str: str
    game_is_paused_str: str
    return_str: str
    back_to_menu_str: str
    save_str: str
    choose_level_str: str
    next_level_str: str
    level_completed_str: str
    restart_str: str

    @abstractmethod
    def __init__(self,
                 localized_strings_name: str,
                 game_name_str: str,
                 start_game_str: str,
                 settings_str: str,
                 background_str: str,
                 language_str: str,
                 music_str: str,
                 start_str: str,
                 back_str: str,
                 game_is_paused_str: str,
                 return_str: str,
                 back_to_menu_str: str,
                 save_str: str,
                 choose_level_str: str,
                 next_level_str: str,
                 level_completed_str: str,
                 restart_str: str):

        self.localized_strings_name = localized_strings_name
        self.game_name_str = game_name_str
        self.start_str = start_str
        self.music_str = music_str
        self.language_str = language_str
        self.background_str = background_str
        self.settings_str = settings_str
        self.start_game_str = start_game_str
        self.back_str = back_str
        self.game_is_paused_str = game_is_paused_str
        self.return_str = return_str
        self.back_to_menu_str = back_to_menu_str
        self.save_str = save_str
        self.choose_level_str = choose_level_str
        self.next_level_str = next_level_str
        self.level_completed_str = level_completed_str
        self.restart_str = restart_str

    @abstractmethod
    def return_new_instance(self):
        return self