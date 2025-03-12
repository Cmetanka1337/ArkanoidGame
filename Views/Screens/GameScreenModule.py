import pygame
from pygame import Rect
from pygame_gui import UI_BUTTON_PRESSED
from pygame_gui.elements import UILabel, UIButton

from Models.LevelManager import LevelManager
from Views.AdditionalBallsBonus import AdditionalBallsBonus
from Views.Ball import BallObject
from Views.Screens.PauseScreenModule import PauseScreen
from Views.UserPlate import UserPlateObject
from Views.Abstract_classes.AbstractScreenModule import AbstractScreen
from Views.Screens.LevelEndScreen import LevelEndScreen

class GameScreen(AbstractScreen):

    def __init__(self, manager, window_surface, clock, selected_level):
        super().__init__(manager, window_surface)
        self.window_width = window_surface.get_width()
        self.window_height = window_surface.get_height()
        self.selected_level = selected_level
        self.elements = []
        self.is_running = True
        self.level_manager = LevelManager(self.window_width, self.window_height)
        self.level_manager.load_level(self.selected_level)
        self.initialize_game_elements()
        self.run_game(clock)

    def update1(self, time_delta):
        if not self.level_manager.blocks:
            print("Рівень завершено! Показуємо LevelEndScreen.")  # Додай для перевірки
            self.show_level_end_screen()

    def show_level_end_screen(self):
        level_end_screen = LevelEndScreen(self.window_surface, self.manager, self.selected_level)
        result = level_end_screen.run()

        if result == "next":
            self.next_level()
        elif result == "retry":
            self.restart_level()
        elif result == "menu":
            self.is_running = False  # Вихід в меню

    def next_level(self):
        if self.selected_level < 2:
            self.selected_level += 1
            self.level_manager.load_level(self.selected_level)
            self.initialize_game_elements()
        else:
            self.is_running = False  # Завершення гри після останнього рівня

    def restart_level(self):
        self.level_manager.load_level(self.selected_level)
        self.initialize_game_elements()
    def initialize_game_elements(self):
        self.plate = UserPlateObject(400, 500, 200, 50, pygame.Color(127, 127, 127), 20)
        self.balls = [BallObject(200, 100, 10, 10, pygame.Color(255, 0, 0), 5, [1, 1], 5, True)]
        self.additional_balls_bonus = AdditionalBallsBonus(300, 100, 20, 20, pygame.Color(255, 0, 0), 5, [0, 1], 5,
                                                           False, 2)

    def process_events(self, event):
        if event.type == UI_BUTTON_PRESSED and event.ui_element == self.pause_button:
            return "menu"
        return None

    def layout_elements(self):
        pause_button_rect = Rect(20, 20, 40, 40)
        self.pause_button = UIButton(
            relative_rect=pause_button_rect,
            text="||",
            manager=self.manager
        )
        self.elements.append(self.pause_button)

        hp_rect = Rect((self.window_width // 2 - 100, 20), (200, 70))
        self.hp_label = UILabel(
            relative_rect=hp_rect,
            text="HP: 4",
            manager=self.manager
        )
        self.elements.append(self.hp_label)



    def run_game(self, clock):
        self.layout_elements()
        paused = False
        pause_screen = None

        while self.is_running:
            time_delta = clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

                self.manager.process_events(event)

                if event.type == UI_BUTTON_PRESSED and event.ui_element == self.pause_button:
                    paused = not paused
                    if paused:
                        pause_screen = PauseScreen(self.window_surface, self.manager)
                    else:
                        if pause_screen:
                            pause_screen.destroy()
                            pause_screen = None

                if paused and pause_screen:
                    result = pause_screen.process_events(event)
                    if result == "game":
                        paused = False
                        pause_screen.destroy()
                        pause_screen = None
                    elif result == "menu":
                        self.destroy()
                        self.is_running = False

            if not paused:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT]:
                    self.plate.move_to(self.plate.rect.x - self.plate.speed, self.plate.rect.y)
                if keys[pygame.K_RIGHT]:
                    self.plate.move_to(self.plate.rect.x + self.plate.speed, self.plate.rect.y)

                self.window_surface.fill((0, 0, 0))
                self.update1(time_delta)

                for ball in self.balls:
                    ball.update_position()
                    ball.calculate_reflection(self.plate, self.level_manager)
                    ball.render(self.window_surface)

                for block in self.level_manager.blocks:
                    block.render(self.window_surface)

                self.additional_balls_bonus.calculate_reflection(self.plate, self)
                self.additional_balls_bonus.update_position()
                self.additional_balls_bonus.render(self.window_surface)

                self.plate.render(self.window_surface)

            else:
                pause_screen.draw()

            self.manager.update(time_delta)
            self.manager.draw_ui(self.window_surface)

            pygame.display.flip()
