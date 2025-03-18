from abc import ABC, abstractmethod

class LocalizedStrings(ABC):

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

    @abstractmethod
    def __init__(self,
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
                 save_str: str):

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
