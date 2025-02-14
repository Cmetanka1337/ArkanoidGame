import os
import pygame_gui
import pygame
from pygame_gui import UIManager, UI_BUTTON_PRESSED

class MenuScreen:

    def __init__(self, manager, window_surface):
        self.background = pygame.Surface(window_surface.get_size())
        self.background.fill('LavenderBlush')

        # Заголовок
        label_rect = pygame.Rect(0, 100, 200, 50)
        label_rect.centerx = window_surface.get_width() // 2
        self.label = pygame_gui.elements.UILabel(
            relative_rect=label_rect,
            text="Arkanoid Game",
            manager=manager
        )

        # Кнопка старту гри
        start_button_rect = pygame.Rect(0, label_rect.bottom + 10, 200, 50)
        start_button_rect.centerx = window_surface.get_width() // 2
        self.start_button = pygame_gui.elements.UIButton(
            relative_rect=start_button_rect,
            text="Start Game",
            manager=manager
        )

        # Кнопка налаштувань
        settings_button_rect = pygame.Rect(0, start_button_rect.bottom + 10, 200, 50)
        settings_button_rect.centerx = window_surface.get_width() // 2
        self.settings_button = pygame_gui.elements.UIButton(
            relative_rect=settings_button_rect,
            text="Settings",
            manager=manager
        )

        # self.draw(manager, window_surface)


    def process_events(self, event):
            """ Обробка натискань кнопок """
            if event.type == UI_BUTTON_PRESSED:
                if event.ui_element == self.start_button:
                    return "game"  # Перехід до гри
                elif event.ui_element == self.settings_button:
                    return "settings"  # Перехід до налаштувань
            return None

    def draw(self, manager, window_surface):
        """ Малюємо меню на екрані """
        window_surface.blit(self.background, (0, 0))
        manager.draw_ui(window_surface)

# separate method for configuring buttons
# method to create and configure window
# method for configuring level(blocks, plates)
# etc



    # def configure_screen(self):
    #     pygame.init()
    #
    #     pygame.display.set_caption("Test Menu Screen")
    #     window_surface = pygame.display.set_mode((800, 600))
    #
    #     theme_path = os.path.join(os.getcwd(), "themes.json")
    #     print(theme_path)
    #     manager = UIManager(window_surface.get_size(), theme_path)
    #
    #     background = pygame.Surface(window_surface.get_size())
    #     background.fill('LavenderBlush')
    #
    #     label_rect = pygame.Rect(0, 100, 200, 150)
    #     label_rect.centerx = window_surface.get_width() // 2
    #     label = pygame_gui.elements.UILabel(
    #         relative_rect=label_rect,
    #         text="Arkanoid Game",
    #         manager=manager
    #     )
    #
    #     start_button_rect = pygame.Rect(0, label_rect.bottom + 10, 200, 50)
    #     start_button_rect.centerx = window_surface.get_width() // 2
    #     start_button = pygame_gui.elements.UIButton(
    #         relative_rect=start_button_rect,
    #         text="Start Game",
    #         manager=manager
    #     )
    #
    #     settings_button_rect = pygame.Rect(0, start_button_rect.bottom + 10, 200, 50)
    #     settings_button_rect.centerx = window_surface.get_width() // 2
    #     settings_button = pygame_gui.elements.UIButton(
    #         relative_rect=settings_button_rect,
    #         text="Settings",
    #         manager=manager
    #     )
    #
    #     clock = pygame.time.Clock()
    #     is_running = True
    #
    #     while is_running:
    #         time_delta = clock.tick(60) / 1000.0
    #         for event in pygame.event.get():
    #             if event.type == pygame.QUIT:
    #                 is_running = False
    #
    #             if event.type == UI_BUTTON_PRESSED:
    #                 if event.ui_element == start_button:
    #                     print("Starting game")
    #
    #             manager.process_events(event)
    #
    #         manager.update(time_delta)
    #
    #         window_surface.blit(background, (0, 0))
    #         manager.draw_ui(window_surface)
    #
    #         pygame.display.update()