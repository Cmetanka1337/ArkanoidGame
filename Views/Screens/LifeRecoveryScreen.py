import time
import pygame
from pygame import Rect
from pygame_gui import UI_BUTTON_PRESSED
from pygame_gui.elements import UILabel, UIButton

from Views.Abstract_classes.AbstractScreenModule import AbstractScreen
class LifeRecoveryScreen(AbstractScreen):

    def __init__(self, window_surface, manager, reset_lives_callback):
        super().__init__(manager, window_surface)
        self.result = None
        self.reset_lives_callback = reset_lives_callback
        self.elements = []
        self.layout_elements()

    def layout_elements(self):
        label_rect = Rect((self.window_surface.get_width() // 2 - 100, 50), (300, 50))
        self.label = UILabel(relative_rect=label_rect, text="Відновлення життя...", manager=self.manager)
        self.elements.append(self.label)

        menu_button_rect = Rect((self.window_surface.get_width() // 2 - 100, 120), (200, 50))
        self.menu_button = UIButton(relative_rect=menu_button_rect, text="Повернутись в меню", manager=self.manager)
        self.elements.append(self.menu_button)

        # Таймер відновлення життя через певний час
        self.recovery_time = time.time() + 5  # 5 секунд для відновлення життя

    def process_events(self, event):
        if event.type == UI_BUTTON_PRESSED and event.ui_element == self.menu_button:
            self.result = "menu"  # Повернутись в головне меню
        self.manager.process_events(event)
        return None

    def run(self):
        clock = pygame.time.Clock()
        while self.result is None:
            time_delta = clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == UI_BUTTON_PRESSED:
                    if event.ui_element == self.menu_button:
                        self.result = "menu"  # Повернутись в меню

                # Обробка подій UI менеджера
                self.manager.process_events(event)

            # Відновлення життя через таймер
            if time.time() > self.recovery_time and self.result is None:
                self.reset_lives_callback()  # Викликаємо функцію для відновлення життя
                self.result = "retry"  # Гравець може спробувати ще раз

            # Оновлення та малювання інтерфейсу
            self.manager.update(time_delta)
            self.manager.draw_ui(self.window_surface)
            pygame.display.flip()

        self.destroy()
        return self.result

    def destroy(self):
        # Логіка очищення екрану, видалення елементів інтерфейсу
        for element in self.elements:
            element.kill()  # Якщо є елементи UI, видалити їх
        print("LifeRecoveryScreen очищено.")

