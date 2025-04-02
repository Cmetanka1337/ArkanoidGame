import pygame
from pygame import Rect
from pygame_gui import UI_BUTTON_PRESSED
from pygame_gui.elements import UIButton, UILabel
from Views.Abstract_classes.AbstractScreenModule import AbstractScreen
class GameOverScreen(AbstractScreen):

    def __init__(self, window_surface, manager, level):
        super().__init__(manager, window_surface)
        self.level = level  # Зберігаємо вибраний рівень
        self.result = None
        self.elements = []
        self.layout_elements()

    def layout_elements(self):
        from Controllers import GameModule
        label_rect = Rect((self.window_surface.get_width() // 2 - 100, 50), (200, 50))
        self.label = UILabel(relative_rect=label_rect, text=GameModule.selected_language.game_over_str, manager=self.manager)
        self.elements.append(self.label)

        retry_button_rect = Rect((self.window_surface.get_width() // 2 - 100, 120), (200, 50))
        self.retry_button = UIButton(relative_rect=retry_button_rect, text=GameModule.selected_language.restart_str, manager=self.manager)
        self.elements.append(self.retry_button)

        menu_button_rect = Rect((self.window_surface.get_width() // 2 - 100, 190), (200, 50))
        self.menu_button = UIButton(relative_rect=menu_button_rect, text=GameModule.selected_language.back_to_menu_str, manager=self.manager)
        self.elements.append(self.menu_button)

    def run(self):
        clock = pygame.time.Clock()
        while self.result is None:
            time_delta = clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == UI_BUTTON_PRESSED:
                    if event.ui_element == self.retry_button:
                        return # нам треба просто повернутись з цього методу у випадку перезапуску. що ти повернеш не буде мати ніякого значення
                    elif event.ui_element == self.menu_button:
                        return "menu"  # Повернення в меню

                    print(f"Button pressed: {self.result}")  # Debugging: which button was pressed

                self.manager.process_events(event)

            self.manager.update(time_delta)
            self.manager.draw_ui(self.window_surface)
            pygame.display.flip()

        print(f"GameOverScreen ended with result: {self.result}")  # Debugging result
        self.destroy()
        return self.result

    def process_events(self, event):
        if event.type == UI_BUTTON_PRESSED:
            if event.ui_element == self.retry_button:
                self.result = "retry"  # Перезапуск гри
            elif event.ui_element == self.menu_button:
                self.result = "menu"  # Повернення в меню

            print(f"Button pressed: {self.result}")  # Log the button press

        self.manager.process_events(event)
        return None

    def destroy(self):
        for element in self.elements:
            element.kill()
        self.result = None
        print("GameOverScreen cleaned up.")  # Debugging cleanup

