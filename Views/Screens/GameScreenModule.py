import pygame
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


class GameScreen(AbstractScreen):

    def __init__(self, manager, window_surface, clock,selected_level):
        super().__init__(manager, window_surface)
        self.hp = None
        self.selected_level = selected_level
        self.elements = []
        self.is_running = True
        self.run_game(clock)
        


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

        self.hp = 4
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
        level_manager = LevelManager(self.window_width, self.window_height)
        level_manager.load_level(self.selected_level)
        plate = UserPlateObject(400, 500, 200, 50, pygame.Color(127, 127, 127), 20)
        ball1 = BallObject(200, 100, 10, 10, pygame.Color(255, 0, 0), 5, [1, 1], 5,True)
        additional_balls_bonus = AdditionalBallsBonus(300,100,20,20,pygame.Color(255, 0, 0), 5, [0,1], 5,False,2)
        extend_platform_bonus = ExtendPlatformBonus(300,100,20,20,pygame.Color(255, 0, 0), 5, [0,1], 5,False,10,400)
        extend_platform_bonus.activate(plate)
        self.balls = [] #added array of balls on the screen
        self.balls.append(ball1)
        #additional_balls_bonus.activate(self)
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
                    plate.move_to(plate.rect.x - plate.speed, plate.rect.y)
                if keys[pygame.K_RIGHT]:
                    plate.move_to(plate.rect.x + plate.speed, plate.rect.y)

                self.window_surface.blit(self.background, (0, 0))
                for ball in self.balls:
                    ball.update_position(self)
                    ball.calculate_reflection(plate,level_manager)
                    #віднімання хп коли мяч вилітає за межі екрану
                    if ball.y_position - ball.radius > self.window_height:
                        self.hp -= 1
                        self.hp_label.set_text("HP: " + str(self.hp))
                        self.balls.remove(ball)

            else:
                pause_screen.draw()

            for ball in self.balls:
                ball.render(self.window_surface)

            for block in level_manager.blocks:
                block.render(self.window_surface)

            if extend_platform_bonus.is_active:
                extend_platform_bonus.update(plate)
                extend_platform_bonus.calculate_reflection(plate, self)
                extend_platform_bonus.update_position()
                extend_platform_bonus.render(self.window_surface)

            if additional_balls_bonus.is_active:
                additional_balls_bonus.calculate_reflection(plate, self)
                additional_balls_bonus.update_position()
                additional_balls_bonus.render(self.window_surface)

            plate.render(self.window_surface)


            self.manager.update(time_delta)
            self.manager.draw_ui(self.window_surface)

            pygame.display.flip()