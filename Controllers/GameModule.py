import os

import pygame
from pygame import Surface
from pygame_gui import UIManager
from pygame_gui.core.interfaces import IUIManagerInterface
from Controllers.SettingsControllerModule import SettingsController
from Models.LocalizedStringEnglish import LocalizedStringEnglish
from Models.LocalizedStrings import LocalizedStrings
from Views.Screens.LevelSelectionModule import LevelSelection

from Views.Screens.SettingsScreenModule import SettingsScreen
from Views.Screens.GameScreenModule import GameScreen
from Views.Screens.MainMenuScreenModule import MenuScreen
from Views.Screens.LevelEndScreen import LevelEndScreen

selected_language: LocalizedStrings = LocalizedStringEnglish()
selected_theme: str = "blue_theme.json"

class Game:
    manager: IUIManagerInterface
    window_surface: Surface

    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        pygame.display.set_caption("Arkanoid Game")

        base_path = os.path.dirname(__file__)
        music_path = os.path.join(base_path, "../Assets/sounds/background_music.mp3")
        theme_path = os.path.join(base_path, "../Assets/Themes", selected_theme)
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.15)

        self.window_surface = pygame.display.set_mode((800, 600))

        self.manager = UIManager(self.window_surface.get_size(), theme_path)
        self.launch_game(self.manager)

    def launch_game(self, manager):
        clock = pygame.time.Clock()
        is_running = True
        current_screen = MenuScreen(manager, self.window_surface)
        selected_level = None

        while is_running:
            time_delta = clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False
                new_screen = current_screen.process_events(event)
                if new_screen:
                    manager.clear_and_reset()
                    if new_screen == "menu":
                        manager = UIManager(self.window_surface.get_size(), f"../Assets/{selected_theme}")
                        current_screen = MenuScreen(self.manager, self.window_surface)
                    if new_screen == "game":
                        selected_level = current_screen.selected_level
                        GameScreen(manager, self.window_surface, clock,
                                                    selected_level=selected_level)
                        current_screen = MenuScreen(manager, self.window_surface)

                    elif new_screen == "level_end":

                        current_screen = LevelEndScreen(self.window_surface, manager, selected_level)

                        result = current_screen.run()

                        if result == "next":

                            selected_level += 1

                            current_screen = GameScreen(manager, self.window_surface, clock,
                                                        selected_level=selected_level)


                        elif result == "retry":
                            current_screen = GameScreen(manager, self.window_surface, clock,
                                                        selected_level)

                        elif result == "menu":
                            current_screen = MenuScreen(manager, self.window_surface)



                    elif new_screen == "settings":
                        settings_controller = SettingsController()
                        settings_controller.volume = pygame.mixer.music.get_volume()
                        settings_controller.background_color = selected_theme
                        current_screen = SettingsScreen(manager, self.window_surface, settings_controller)

                    elif new_screen == "menu":
                        current_screen = MenuScreen(manager, self.window_surface)
                    elif new_screen == "lvl_selection":
                        current_screen = LevelSelection(manager, self.window_surface)
                        selected_level = current_screen.selected_level

                manager.process_events(event)



            manager.update(time_delta)
            current_screen.draw()
            pygame.display.update()

game = Game()