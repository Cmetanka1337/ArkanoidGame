import pytest
import pygame
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Views.UserPlate import UserPlateObject


@pytest.fixture
def user_plate():
    pygame.init()
    return UserPlateObject(x_position=50, y_position=60, width=100, height=20,
                           color=pygame.Color(255, 0, 0), speed=5)

@pytest.mark.parametrize("x_input,expected_x", [
    (10, 10),
    (-50, 0),
    (2000, 800),  # Припустимо, ширина сцени 900, об'єкт 100
])
def test_move_to(user_plate, x_input, expected_x):
    user_plate.scene_width = 900
    user_plate.move_to(x_input, 60)
    assert user_plate.rect.x == expected_x
    assert user_plate.rect.y == 60

def test_resize_within_bounds(user_plate):
    user_plate.scene_width = 900
    user_plate.rect.x = 100
    user_plate.resize(300)
    assert user_plate.rect.width == 300

def test_resize_exceeding_bounds(user_plate):
    user_plate.scene_width = 200
    user_plate.rect.x = 100
    user_plate.resize(150)
    # Перевіримо, що він не вийшов за межі
    assert user_plate.rect.x == 50
    assert user_plate.rect.width == 150

def test_render_mock_pytest_mocker(mocker, user_plate):
    screen = mocker.Mock()
    draw_mock = mocker.patch("pygame.draw.rect")
    user_plate.render(screen)
    draw_mock.assert_called_once_with(screen, user_plate.color, user_plate.rect)
