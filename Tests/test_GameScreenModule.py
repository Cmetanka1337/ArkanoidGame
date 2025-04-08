import sys
import os

from pygame_gui import UI_BUTTON_PRESSED, UIManager

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
import pygame
from unittest.mock import Mock, patch
from Views.Screens.GameScreenModule import GameScreen
from Views.UserPlate import UserPlateObject
from Views.Ball import BallObject

pygame.init()

# Фікстура для створення GameScreen
@pytest.fixture
def game_screen():
    pygame.init()
    window_surface = pygame.display.set_mode((800, 600))
    manager = UIManager((800, 600))   # Справжній UIManager
    screen = GameScreen(manager=manager, window_surface=window_surface, clock=pygame.time.Clock(), selected_level=Mock(), hp=5)
    yield screen
    pygame.quit()

# Тест ініціалізації
# def test_init(game_screen):
#     assert game_screen.hp == 5
#     assert game_screen.window_width == 800
#     assert game_screen.window_height == 600
#     assert game_screen.selected_level == 1
#     assert game_screen.is_running is True
#
# # Тест для initialize_game_elements
# def test_initialize_game_elements(game_screen):
#     game_screen.initialize_game_elements()
#     assert isinstance(game_screen.plate, UserPlateObject)
#     assert len(game_screen.balls) == 1
#     assert isinstance(game_screen.balls[0], BallObject)
#
# # Тест для process_events
# def test_process_events(game_screen):
#     game_screen.layout_elements()  # Створюємо UI-елементи
#     pause_button = game_screen.pause_button
#
#     # Створюємо фейкову подію натискання кнопки паузи
#     event = pygame.event.Event(UI_BUTTON_PRESSED, {'ui_element': pause_button, 'ui_object_id': pause_button.most_specific_combined_id})
#
#     result = game_screen.process_events(event)
#     assert result == "menu"