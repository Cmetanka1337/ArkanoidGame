import pytest
import pygame
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Views.LevelPlate import LevelPlateObject

@pytest.fixture
def level_plate(mocker):
    mock_level_manager = mocker.Mock()
    pygame.init()
    return LevelPlateObject(
        hit_points=3,
        plate_type='standard',
        is_breakable=True,
        x_position=100,
        y_position=100,
        width=50,
        height=20,
        color=pygame.Color(255, 0, 0),
        is_visible=True,
        level_manager=mock_level_manager
    )

def test_render(mocker, level_plate):
    screen = mocker.Mock()
    surface_mock = mocker.patch("pygame.Surface")
    level_plate.render(screen)
    surface_mock.assert_called_once()

def test_destroy_platform_calls_level_manager(level_plate):
    level_plate.destroy_platform()
    level_plate.level_manager.remove_block.assert_called_once_with(level_plate)

@pytest.mark.parametrize("hit_points, expected_visible, expected_alpha", [
    (3, True, 170),
    (2, True, 85),
    (1, False, 255),  # when hit_points = 1, it becomes invisible
])
def test_decrease_hit_points_behavior(mocker, hit_points, expected_visible, expected_alpha,level_plate):

    level_plate.hit_points = hit_points
    level_plate.decrease_hit_points()
    assert level_plate.is_visible == expected_visible
    assert level_plate.alpha == expected_alpha or plate.alpha == 255  # 255 for the bonus case

def test_decrease_hit_points_bonus_addition(mocker,level_plate):

    level_plate.plate_type = 'bonus'
    bonus_mock = mocker.Mock()
    mocker.patch("Views.LevelPlate.LevelPlateObject.spawn_bonus", return_value=bonus_mock)
    level_plate.decrease_hit_points()
    assert bonus_mock in level_plate.active_bonuses
    assert not level_plate.is_visible

def test_spawn_bonus_returns_extend_platform(mocker, level_plate):
    level_plate.plate_type = 'bonus'

    # Мокаємо ExtendPlatformBonus і AdditionalBallsBonus безпосередньо
    mock_extend = mocker.patch("Views.ExtendPlatformBonus.ExtendPlatformBonus", autospec=True)
    mock_additional = mocker.patch("Views.AdditionalBallsBonus.AdditionalBallsBonus", autospec=True)

    # Мокаємо random.choice, щоб повертав mock_extend
    mocker.patch("random.choice", return_value=mock_extend)

    # Викликаємо spawn_bonus
    bonus = level_plate.spawn_bonus()

    # Перевіряємо, чи є bonus екземпляром правильного класу
    assert isinstance(bonus, mock_extend.return_value.__class__)


def test_spawn_bonus_returns_additional_balls(mocker, level_plate):
    level_plate.plate_type = 'bonus'

    # Мокаємо ExtendPlatformBonus і AdditionalBallsBonus безпосередньо
    mock_extend = mocker.patch("Views.ExtendPlatformBonus.ExtendPlatformBonus", autospec=True)
    mock_additional = mocker.patch("Views.AdditionalBallsBonus.AdditionalBallsBonus", autospec=True)

    # Мокаємо random.choice, щоб повертав mock_additional
    mocker.patch("random.choice", return_value=mock_additional)

    # Викликаємо spawn_bonus
    bonus = level_plate.spawn_bonus()

    # Перевіряємо, чи є bonus екземпляром правильного класу
    assert isinstance(bonus, mock_additional.return_value.__class__)




def test_update_state_fades_out(level_plate):
    level_plate.is_visible = False
    level_plate.alpha = 30
    level_plate.update_state()
    assert level_plate.alpha == 20
    level_plate.update_state()
    assert level_plate.alpha == 10
    level_plate.update_state()
    assert level_plate.alpha == 0