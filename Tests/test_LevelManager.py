import pytest
import pygame
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Views.LevelPlate import LevelPlateObject
from Models.LevelManager import LevelManager


@pytest.fixture
def level_manager():
    pygame.init()
    return LevelManager(screen_width=800, screen_height=600)


def test_initialization(level_manager):
    assert level_manager.screen_width == 800
    assert level_manager.screen_height == 600
    assert level_manager.blocks == []


def test_load_level_1(level_manager, mocker):
    # Підмінюємо метод generate_letter_A, щоб перевірити, що він викликається
    mock_generate_letter_A = mocker.patch.object(level_manager, 'generate_letter_A')
    level_manager.load_level(1)
    mock_generate_letter_A.assert_called_once()
    assert level_manager.blocks == []  # Перевіряємо, що blocks було очищено


def test_load_level_2(level_manager, mocker):
    # Підмінюємо метод generate_rhombus, щоб перевірити, що він викликається
    mock_generate_rhombus = mocker.patch.object(level_manager, 'generate_rhombus')
    level_manager.load_level(2)
    mock_generate_rhombus.assert_called_once()
    assert level_manager.blocks == []  # Перевіряємо, що blocks було очищено


def test_add_vertical_lines(level_manager):
    # Використовуємо реальні об'єкти замість моків
    center_x = 400
    center_y = 300
    rows = 3
    block_width = 50
    block_height = 20
    side_blocks = 2

    # Очищаємо блоки перед тестом
    level_manager.blocks = []

    level_manager.add_vertical_lines(center_x, center_y, rows, block_width, block_height, side_blocks)

    # Перевіряємо, що створено правильну кількість блоків
    # 2 сторони * 2 side_blocks = 4 блоки
    assert len(level_manager.blocks) == 4


def test_generate_rhombus(level_manager, mocker):
    # Мокуємо метод add_vertical_lines, щоб зосередитись на логіці generate_rhombus
    mocker.patch.object(level_manager, 'add_vertical_lines')

    # Очищаємо блоки перед тестом
    level_manager.blocks = []

    level_manager.generate_rhombus()

    # Перевіряємо, що було створено блоки
    # У ромбі має бути як мінімум кілька блоків (точну кількість важко підрахувати через логіку)
    assert len(level_manager.blocks) > 0


def test_generate_letter_A(level_manager, mocker):
    # Мокуємо метод add_vertical_lines, щоб зосередитись на логіці generate_letter_A
    mocker.patch.object(level_manager, 'add_vertical_lines')

    # Очищаємо блоки перед тестом
    level_manager.blocks = []

    level_manager.generate_letter_A()

    # Перевіряємо, що було створено блоки
    assert len(level_manager.blocks) > 0


def test_remove_block(level_manager):
    # Створюємо тестовий блок
    test_block = LevelPlateObject(
        hit_points=3,
        plate_type="standard",
        is_breakable=True,
        x_position=100,
        y_position=100,
        height=20,
        width=50,
        color=pygame.Color(255, 0, 0),
        level_manager=level_manager
    )

    # Додаємо блок до списку
    level_manager.blocks.append(test_block)
    assert len(level_manager.blocks) == 1

    # Видаляємо блок
    level_manager.remove_block(test_block)
    assert len(level_manager.blocks) == 0


def test_remove_nonexistent_block(level_manager):
    # Створюємо тестовий блок, але не додаємо його до списку
    test_block = LevelPlateObject(
        hit_points=3,
        plate_type="standard",
        is_breakable=True,
        x_position=100,
        y_position=100,
        height=20,
        width=50,
        color=pygame.Color(255, 0, 0),
        level_manager=level_manager
    )

    # Переконуємося, що список порожній
    assert len(level_manager.blocks) == 0

    # Спроба видалити блок, якого немає в списку, не повинна викликати помилку
    level_manager.remove_block(test_block)
    assert len(level_manager.blocks) == 0


def test_render(level_manager, mocker):
    # Мокаємо екран і метод render для LevelPlateObject
    mock_screen = mocker.Mock()

    # Створюємо два тестових блоки з мокованим методом render
    test_block1 = mocker.Mock()
    test_block2 = mocker.Mock()

    # Додаємо блоки до списку
    level_manager.blocks = [test_block1, test_block2]

    # Викликаємо метод render
    level_manager.render(mock_screen)

    # Перевіряємо, що render кожного блоку був викликаний із правильним аргументом
    test_block1.render.assert_called_once_with(mock_screen)
    test_block2.render.assert_called_once_with(mock_screen)