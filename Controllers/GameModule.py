import pygame
from pygame import Surface
from pygame_gui import UIManager
from pygame_gui.core.interfaces import IUIManagerInterface
from Controllers.SceneModule import SceneObject
from Views.Screens.LevelSelectionModule import LevelSelection
from Views.Screens.LifeRecoveryScreen import LifeRecoveryScreen
from Views.Screens.SettingsScreenModule import SettingsScreen
from Views.Screens.GameScreenModule import GameScreen
from Views.Screens.MainMenuScreenModule import MenuScreen
from Views.Screens.LevelEndScreen import LevelEndScreen


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
        print(pygame.font.get_fonts())
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
        selected_level = None  # Додаємо змінну для відстеження рівня

        while is_running:
            time_delta = clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False

                new_screen = current_screen.process_events(event)
                if new_screen:
                    manager.clear_and_reset()
                    if new_screen == "game":
                        selected_level = current_screen.selected_level
                        current_screen = GameScreen(manager, self.window_surface, clock,
                                                    selected_level=selected_level)
                        manager.clear_and_reset()
                        current_screen = MenuScreen(manager, self.window_surface)
                    elif new_screen == "level_end":
                        current_screen = LevelEndScreen(self.window_surface, manager, selected_level)

                        result = current_screen.run()  # ОЧІКУЄМО ВИБОРУ КОРИСТУВАЧА

                        print(f"Гравець вибрав: {result}")  # Додаємо перевірку результату

                        if result == "next":
                            selected_level += 1
                            current_screen = GameScreen(manager, self.window_surface, clock,
                                                        selected_level=selected_level)

                        elif result == "retry":
                            current_screen = GameScreen(manager, self.window_surface, clock,
                                                        selected_level)

                        elif result == "menu":
                            current_screen = MenuScreen(manager, self.window_surface)

                    # по-моєму, код нижче взагалі нічого не робить
                    # elif new_screen == "game_over":
                    #
                    #     print("Game Over — всі м'ячі зникли")  # Debug
                    #
                    #     current_screen = GameOverScreen(self.window_surface, manager, selected_level)
                    #
                    #     result = current_screen.run()
                    #
                    #     if result == "retry":
                    #
                    #         print("Гравець вирішив повторити рівень")  # Debug
                    #
                    #         current_screen = GameScreen(manager, self.window_surface, clock, selected_level)
                    #         current_screen.run() # клас GameScreen не має методу run
                    #
                    #
                    #     elif result == "menu":
                    #
                    #         print("Гравець повернувся в меню")  # Debug
                    #
                    #         current_screen = MenuScreen(manager, self.window_surface)

                    elif new_screen == "life_recovery":
                        # Викликаємо екран відновлення життя
                        current_screen = LifeRecoveryScreen(self.window_surface, manager)

                        result = current_screen.run()  # Очікуємо результат вибору користувача

                        if result == "retry":
                            # Перезапускаємо гру
                            current_screen = GameScreen(manager, self.window_surface, clock,
                                                        selected_level=selected_level)

                        elif result == "menu":
                            # Повертаємось в меню
                            current_screen = MenuScreen(manager, self.window_surface)

                    elif new_screen == "settings":
                        current_screen = SettingsScreen(manager, self.window_surface)
                    elif new_screen == "menu":
                        current_screen = MenuScreen(manager, self.window_surface)
                    elif new_screen == "lvl_selection":
                        current_screen = LevelSelection(manager, self.window_surface)
                        selected_level = current_screen.selected_level

                manager.process_events(event)

            manager.update(time_delta)
            current_screen.draw()
            pygame.display.update()
Game()