import pygame
from pygame import Rect
from pygame_gui import UI_BUTTON_PRESSED
from pygame_gui.elements import UIButton, UILabel
from Views.Abstract_classes.AbstractScreenModule import AbstractScreen

class LevelEndScreen(AbstractScreen):

    def __init__(self, window_surface, manager, level):
        super().__init__(manager, window_surface)
        self.level = level
        self.result = None
        self.elements = []
        self.layout_elements()

    def layout_elements(self):
        from Controllers import GameModule
        label_rect = Rect((self.window_surface.get_width() // 2 - 100, 50), (250, 50))
        self.label = UILabel(
            relative_rect=label_rect,
            text=GameModule.selected_language.level_completed_str,
            manager=self.manager)
        self.elements.append(self.label)

        next_button_rect = Rect((self.window_surface.get_width() // 2 - 100, 120), (200, 50))
        self.next_button = UIButton(
            relative_rect=next_button_rect,
            text=GameModule.selected_language.next_level_str,
            manager=self.manager)
        self.elements.append(self.next_button)

        retry_button_rect = Rect((self.window_surface.get_width() // 2 - 100, 190), (200, 50))
        self.retry_button = UIButton(
            relative_rect=retry_button_rect,
            text=GameModule.selected_language.restart_str,
            manager=self.manager)
        self.elements.append(self.retry_button)

        menu_button_rect = Rect((self.window_surface.get_width() // 2 - 100, 260), (200, 50))
        self.menu_button = UIButton(
            relative_rect=menu_button_rect,
            text=GameModule.selected_language.back_to_menu_str,
            manager=self.manager)
        self.elements.append(self.menu_button)

    def run(self):
        clock = pygame.time.Clock()
        while self.result is None:
            time_delta = clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == UI_BUTTON_PRESSED:
                    if event.ui_element == self.next_button:
                        self.result = "next"
                    elif event.ui_element == self.retry_button:
                        self.result = "retry"
                    elif event.ui_element == self.menu_button:
                        self.result = "menu"


                # Обробка подій UI менеджера
                self.manager.process_events(event)

            # Оновлення та малювання інтерфейсу
            self.manager.update(time_delta)
            self.manager.draw_ui(self.window_surface)
            pygame.display.flip()

        self.destroy()
        return self.result

    def process_events(self, event):
        # Обробка подій для кнопок
        if event.type == UI_BUTTON_PRESSED:
            if event.ui_element == self.next_button:
                self.result = "next"
            elif event.ui_element == self.retry_button:
                self.result = "retry"
            elif event.ui_element == self.menu_button:
                self.result = "menu"


        # Залишаємо обробку подій UI менеджера
        self.manager.process_events(event)
        return None

    def destroy(self):
            # Логіка очищення екрану, наприклад, видалення елементів інтерфейсу
            for element in self.elements:
                element.kill()  # Якщо у вас є елементи UI, видалити їх.