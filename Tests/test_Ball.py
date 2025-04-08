import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
import pygame
from unittest.mock import Mock, patch
from Views.Scene import SceneObject
from Views.Ball import BallObject

pygame.init()

@pytest.fixture
def ball():
    return BallObject(
        x_position=100.0,
        y_position=100.0,
        height=20.0,
        width=20.0,
        color=pygame.Color(255, 0, 0),
        speed=2.0,
        move_direction=[1.0, 1.0],
        radius=10.0,
        is_visible=True
    )

@pytest.fixture
def mock_screen():
    return Mock()

@pytest.fixture
def mock_user_plate():
    plate = Mock(spec=["rect"])
    plate.rect = pygame.Rect(90, 110, 50, 10)  # Використовуємо реальний pygame.Rect
    return plate

@pytest.fixture
def mock_level_manager():
    plate = Mock(spec=["rect", "is_visible", "is_breakable", "decrease_hit_points", "update_state"])
    plate.rect = pygame.Rect(80, 90, 40, 10)  # Використовуємо реальний pygame.Rect
    plate.is_visible = True
    plate.is_breakable = True
    plate.decrease_hit_points = Mock()
    plate.update_state = Mock()

    level_manager = Mock()
    level_manager.blocks = [plate]
    level_manager.remove_block = Mock()
    return level_manager


# Тест ініціалізації
def test_init(ball):
    assert ball.x_position == 100.0
    assert ball.y_position == 100.0
    assert ball.speed == 2.0
    assert ball.move_direction == [1.0, 1.0]
    assert ball.radius == 10.0
    assert ball.is_visible is True


# Тест рендерингу
@patch("pygame.draw.circle")
def test_render_visible(mock_circle, ball, mock_screen):
    ball.render(mock_screen)
    mock_circle.assert_called_once_with(mock_screen, ball.color, (100, 100), 10)


# # Тест відбиття від user_plate
# def test_calculate_reflection_with_user_plate(ball, mock_user_plate, mock_level_manager):
#     SceneObject.width = 800
#     SceneObject.height = 600
#     ball.x_position = 100.0
#     ball.y_position = 109.0  # 109 + 10 = 119 >= 110
#     ball.move_direction = [0.0, 1.0]  # Рух вниз
#
#     print(f"Before: x={ball.x_position}, y={ball.y_position}, direction={ball.move_direction}")
#     print(f"Plate: x={mock_user_plate.rect.x}, y={mock_user_plate.rect.y}, width={mock_user_plate.rect.width}")
#     print(f"Check: y + radius = {ball.y_position + ball.radius}, plate.y = {mock_user_plate.rect.y}")
#
#     ball.calculate_reflection(mock_user_plate, mock_level_manager)
#
#     print(f"After: x={ball.x_position}, y={ball.y_position}, direction={ball.move_direction}")
#
#     assert ball.move_direction == [0.0, -1.0]  # Перевіряємо відбиття вгору


# Тест відбиття від платформи рівня
def test_calculate_reflection_with_level_plate(ball, mock_user_plate, mock_level_manager):
    SceneObject.width = 800
    SceneObject.height = 600
    ball.x_position = 90.0  # У межах платформи (80 <= 90 <= 120)
    ball.y_position = 95.0  # У межах по Y (90 - 10 <= 95 <= 100 + 10)
    ball.move_direction = [0.0, 1.0]  # Рух вниз

    print(f"Before: x={ball.x_position}, y={ball.y_position}, direction={ball.move_direction}")
    print(
        f"Level Plate: x={mock_level_manager.blocks[0].rect.x}, y={mock_level_manager.blocks[0].rect.y}, width={mock_level_manager.blocks[0].rect.width}")

    ball.calculate_reflection(mock_user_plate, mock_level_manager)

    print(f"After: x={ball.x_position}, y={ball.y_position}, direction={ball.move_direction}")

    assert ball.move_direction == [0.0, -1.0]  # Вертикальне відбиття
    mock_level_manager.blocks[0].decrease_hit_points.assert_called_once()
    mock_level_manager.blocks[0].update_state.assert_called_once()

# Тест скидання позиції
@pytest.mark.reset
def test_reset_position(ball):
    SceneObject.width = 800
    SceneObject.height = 600
    ball.reset_position()
    assert ball.x_position == 400
    assert ball.y_position == 550