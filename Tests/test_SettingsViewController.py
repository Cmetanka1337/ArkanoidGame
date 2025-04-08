import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
import pygame
from unittest.mock import Mock, patch
from Models.LocalizedStringEnglish import LocalizedStringEnglish
from Models.LocalizedStrings import LocalizedStrings
from Controllers.SettingsControllerModule import SettingsController

pygame.init()

# Тимчасове створення GameModule у тестах
@pytest.fixture(autouse=True)
def setup_game_module():
    game_module = Mock()
    game_module.selected_theme = "blue_theme.json"
    game_module.selected_language = None
    sys.modules["Controllers.GameModule"] = game_module
    yield
    # Очищення після тестів
    del sys.modules["Controllers.GameModule"]

# Фікстура для створення SettingsController
@pytest.fixture
def settings_controller():
    return SettingsController()

# Тест ініціалізації
def test_init(settings_controller):
    assert settings_controller.background_color == "blue_theme.json"
    assert isinstance(settings_controller.language, LocalizedStringEnglish)
    assert settings_controller.volume == 0.15

# Тест для change_background
def test_change_background(settings_controller):
    from Controllers.GameModule import selected_theme
    settings_controller.change_background("blue_theme.json")
    assert selected_theme == "blue_theme.json"

# Тест для change_language
def test_change_language(settings_controller):
    new_language = Mock(spec=LocalizedStrings)
    settings_controller.change_language(new_language)
    assert settings_controller.language == new_language

# Тест для change_volume з параметризацією
@pytest.mark.parametrize("input_volume, expected_volume", [
    (0.5, 0.5),   # Нормальне значення
    (-0.1, 0.0),  # Менше 0
    (1.5, 1.0),   # Більше 1
])
@patch("pygame.mixer.music")
def test_change_volume(mock_music, settings_controller, input_volume, expected_volume):
    settings_controller.change_volume(input_volume)
    mock_music.set_volume.assert_called_once_with(expected_volume)
    assert settings_controller.volume == expected_volume

# Тест для get_background
def test_get_background(settings_controller):
    settings_controller.change_background("green_theme.json")
    result = settings_controller.get_background()
    assert result == "green_theme.json"

# Тест для get_language
def test_get_language(settings_controller):
    result = settings_controller.get_language()
    assert isinstance(result, LocalizedStringEnglish)

# Тест для get_volume
def test_get_volume(settings_controller):
    result = settings_controller.get_volume()
    assert result == 0.15