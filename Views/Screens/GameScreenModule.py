import pygame
import time
#from main import level_manager
from pygame import Rect
from pygame_gui import UI_BUTTON_PRESSED
from pygame_gui.elements import UILabel, UIButton

from Models.LevelManager import LevelManager
from Views.AdditionalBallsBonus import AdditionalBallsBonus
from Views.Ball import BallObject
from Views.ExtendPlatformBonus import ExtendPlatformBonus

from Views.Screens.PauseScreenModule import PauseScreen
from Views.UserPlate import UserPlateObject
from Views.Abstract_classes.AbstractScreenModule import AbstractScreen
from Views.Abstract_classes.AbstractBonusObject import AbstractBonusObject
from Views.Screens.GameOverScreen import GameOverScreen
from Views.Screens.LevelEndScreen import LevelEndScreen

class GameScreen(AbstractScreen):


    def __init__(self, manager, window_surface, clock, selected_level, hp=5):
        super().__init__(manager, window_surface)
        self.hp = hp
        self.window_width = window_surface.get_width()
        self.window_height = window_surface.get_height()
        self.selected_level = selected_level
        self.elements = []
        self.is_running = True
        self.level_manager = LevelManager(self.window_width, self.window_height)
        self.level_manager.load_level(self.selected_level)
        self.initialize_game_elements()
        self.run_game(clock)

    def checkIfNotBlocks(self, time_delta):
        if not self.level_manager.blocks:
            self.show_level_end_screen()

    def checkIfNotBalls(self, time_delta):
        if len(self.balls) == 0 and self.hp > 0:
            self.show_game_over_screen()

    def show_game_over_screen(self):
        game_over_screen = GameOverScreen(self.window_surface, self.manager, self.selected_level)
        result = game_over_screen.run()

        if result == "menu":
            game_over_screen.destroy()
            self.is_running = False
            return
        else:
            self.restart_level()
            self.is_running = True
        game_over_screen.destroy()

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
        self.destroy()  # Очищаємо поточний рівень
        self.level_manager.load_level(self.selected_level)  # Завантажуємо рівень заново
        self.initialize_game_elements()  # Ініціалізуємо елементи гри
        self.layout_elements()  # Додаємо UI елементи
        self.is_running = True  # Встановлюємо прапорець для продовження гри

    def initialize_game_elements(self):
        self.plate = UserPlateObject(400, 500, 200, 50, pygame.Color(127, 127, 127), 20)
        self.balls = [BallObject(200, 100, 10, 10, pygame.Color(255, 0, 0), 5, [1, 1], 5, True)]
        self.active_bonuses = []

    def process_events(self, event):
        if event.type == UI_BUTTON_PRESSED and event.ui_element == self.pause_button:
            return "menu"
        if len(self.balls) == 0 and self.hp > 0:  # Якщо м’ячі зникли, але життя ще є
            return "game_over"


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
            text=f"HP: {self.hp}",
            manager=self.manager
        )
        self.elements.append(self.hp_label)



    def destroy(self):
        for element in self.elements:
            element.kill()
        self.elements.clear()

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

                # Перевірка на натискання кнопки паузи
                if event.type == UI_BUTTON_PRESSED and event.ui_element == self.pause_button:
                    paused = not paused
                    if paused:
                        pause_screen = PauseScreen(self.window_surface, self.manager)
                    else:
                        if pause_screen:
                            pause_screen.destroy()
                            pause_screen = None

                # if event.type == UI_BUTTON_PRESSED and event.ui_element == self.game_over:
                #     for ball in self.balls[:]:
                #         self.balls.remove(ball)

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

                self.window_surface.blit(self.background, (0, 0))
                self.checkIfNotBlocks(time_delta)
                self.checkIfNotBalls(time_delta)

                # Оновлення м’ячів
                for ball in self.balls[:]:
                    ball.update_position(self)
                    ball.calculate_reflection(self.plate, self.level_manager)
                    if ball.y_position - ball.radius > self.window_height:
                        self.balls.remove(ball)
                        if len(self.balls) == 0:
                            self.hp -= 1
                            self.hp_label.set_text("HP: " + str(self.hp))

                            if self.hp > 0:
                                self.show_game_over_screen()  # Показуємо Game Over Screen

                                if self.is_running:  # Якщо гравець натиснув "retry", перезапускаємо рівень
                                    self.restart_level()  # Викликаємо перезапуск рівня
                                else:
                                    self.destroy()
                                    return
                            else:

                                self.is_running = False  # Завершуємо гру

            else:
                pause_screen.draw()

            # Рендер м’ячів
            for ball in self.balls:
                ball.render(self.window_surface)

            # Рендер блоків рівня
            for block in self.level_manager.blocks[:]:
                block.render(self.window_surface)
                # Якщо блок бонусовий і був зруйнований, спаунити бонус і видалити блок
                if block.plate_type == "bonus" and not block.is_visible:
                    bonus = block.spawn_bonus()  # spawn_bonus повертає об’єкт, похідний від AbstractBonusObject
                    if bonus:
                        self.active_bonuses.append(bonus)
                    self.level_manager.remove_block(block)

            # Оновлення та рендер активних бонусів
            for bonus in self.active_bonuses[:]:

                bonus.calculate_reflection(self.plate, self)
                bonus.update_position()
                bonus.render(self.window_surface)
                if not bonus.is_visible:
                    self.active_bonuses.remove(bonus)

            self.plate.render(self.window_surface)



            self.manager.update(time_delta)
            self.manager.draw_ui(self.window_surface)

            pygame.display.flip()
