import pygame
from pygame import Surface
from pygame_gui import UIManager
from pygame_gui.core.interfaces import IUIManagerInterface
from Controllers.SceneModule import SceneObject
from Views.Screens.SettingsScreenModule import SettingsScreen
from Views.Screens.GameScreenModule import GameScreen
from Views.Screens.MainMenuScreenModule import MenuScreen


class Game:

    end_score: int = 0
    background_color: str
    language: str
    volume: float

    manager: IUIManagerInterface
    window_surface: Surface

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Arkanoid Game")
        self.window_surface = pygame.display.set_mode((800, 600))

        self.manager = UIManager(self.window_surface.get_size(), "../Assets/themes.json")

        self.launch_game(self.manager)

    def start(self):
        pass

    def level_selection(self):
        pass

    def finish_game(self):
        pass

    def draw_scene(self) -> SceneObject:
        pass

    def restart(self):
        pass

    def close(self):
        pass

    def change_background(self):
        pass

    def change_language(self):
        pass

    def change_volume(self):
        pass


    def launch_game(self, manager):
        clock = pygame.time.Clock()
        is_running = True
        current_screen = MenuScreen(manager, self.window_surface)

        while is_running:
            time_delta = clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False

                new_screen = current_screen.process_events(event)
                if new_screen:
                    manager.clear_and_reset()
                    if new_screen == "game":
                        current_screen = GameScreen(manager, self.window_surface)
                    elif new_screen == "settings":
                        current_screen = SettingsScreen(manager, self.window_surface)
                    elif new_screen == "menu":
                        current_screen = MenuScreen(manager, self.window_surface)

                manager.process_events(event)

            manager.update(time_delta)
            current_screen.draw(manager, self.window_surface)
            pygame.display.update()

Game()