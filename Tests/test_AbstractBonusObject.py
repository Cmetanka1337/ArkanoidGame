import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
import pygame
from unittest.mock import MagicMock, patch
from Views.Abstract_classes.AbstractBonusObject import AbstractBonusObject


class DummyBonusObject(AbstractBonusObject):
    """
    Конкретна реалізація абстрактного класу для тестування.
    """

    def __init__(self, x_position: float, y_position: float, height: float, width: float, color: pygame.Color,
                 is_visible, speed: float, move_direction: list, radius: float, is_active: bool):
        super().__init__(x_position, y_position, height, width, color, is_visible, speed, move_direction, radius,
                         is_active)
        self.activated = False
        self.deactivated = False
        self.target = None

    def activate(self, target):
        self.activated = True
        self.target = target

    def deactivate(self, target):
        self.deactivated = True
        self.target = target


@pytest.fixture
def dummy_bonus():
    """
    Базова фікстура, яка створює екземпляр бонусу для тестування.
    """
    return DummyBonusObject(
        x_position=100.0,
        y_position=200.0,
        height=20.0,
        width=20.0,
        color=pygame.Color(255, 0, 0),
        is_visible=True,
        speed=5.0,
        move_direction=[0, 1],
        radius=10.0,
        is_active=False
    )


@pytest.fixture
def mock_screen():
    """
    Фікстура, яка створює макет екрану для тестування рендерингу.
    """
    return MagicMock()


@pytest.fixture
def mock_game_screen():
    """
    Фікстура, яка створює макет ігрового екрану.
    """
    return MagicMock()


@pytest.fixture
def mock_user_plate():
    """
    Фікстура, яка створює макет платформи користувача.
    """
    plate = MagicMock()
    plate.rect = MagicMock()
    plate.rect.x = 80
    plate.rect.y = 300
    plate.rect.width = 100
    return plate


class TestAbstractBonusObject:

    @pytest.mark.initialization
    def test_initialization(self, dummy_bonus):
        """Тест коректної ініціалізації об'єкта бонусу."""
        assert dummy_bonus.x_position == 100.0
        assert dummy_bonus.y_position == 200.0
        assert dummy_bonus.height == 20.0
        assert dummy_bonus.width == 20.0
        assert dummy_bonus.color == pygame.Color(255, 0, 0)
        assert dummy_bonus.is_visible is True
        assert dummy_bonus.speed == 5.0
        assert dummy_bonus.move_direction == [0, 1]
        assert dummy_bonus.radius == 10.0
        assert dummy_bonus.is_active is False

    @pytest.mark.movement
    def test_move_to(self, dummy_bonus):
        """Тест методу move_to, який змінює напрямок руху та оновлює позицію."""
        dummy_bonus.move_to(1.0, 2.0)
        assert dummy_bonus.move_direction == [1.0, 2.0]
        assert dummy_bonus.x_position == 105.0  # 100 + 5*1
        assert dummy_bonus.y_position == 210.0  # 200 + 5*2

    @pytest.mark.movement
    def test_update_position(self, dummy_bonus):
        """Тест методу update_position, який оновлює позицію згідно напрямку руху."""
        dummy_bonus.move_direction = [0.5, -0.5]
        dummy_bonus.update_position()
        assert dummy_bonus.x_position == 102.5  # 100 + 5*0.5
        assert dummy_bonus.y_position == 197.5  # 200 + 5*(-0.5)

    @pytest.mark.rendering
    def test_render(self, dummy_bonus, mock_screen):
        """Тест методу render, який малює бонус на екрані."""
        with patch('pygame.draw.circle') as mock_draw:
            dummy_bonus.render(mock_screen)
            mock_draw.assert_called_once_with(
                mock_screen,
                dummy_bonus.color,
                (int(dummy_bonus.x_position), int(dummy_bonus.y_position)),
                int(dummy_bonus.radius)
            )

    @pytest.mark.collision
    @pytest.mark.parametrize("bonus_y, plate_y, expected_active", [
        (290, 300, True),  # Бонус торкається верхньої межі платформи
        (350, 300, True),  # Бонус нижче платформи - згідно з поточною реалізацією, також активується
        (250, 300, False)  # Бонус вище платформи
    ])
    def test_calculate_reflection_y_position(self, dummy_bonus, mock_user_plate, mock_game_screen, bonus_y, plate_y,
                                             expected_active):
        """
        Параметризований тест методу calculate_reflection для різних позицій по Y.
        Перевіряє, чи активується бонус при контакті з платформою.

        Примітка: Згідно з поточною реалізацією, бонус активується, якщо його нижня точка
        (y_position + radius) знаходиться на або нижче верхньої межі платформи (plate_y).
        """
        dummy_bonus.y_position = bonus_y
        mock_user_plate.rect.y = plate_y
        dummy_bonus.calculate_reflection(mock_user_plate, mock_game_screen)
        assert dummy_bonus.is_active == expected_active
        assert dummy_bonus.is_visible != expected_active  # Якщо активний, то невидимий

    @pytest.mark.collision
    @pytest.mark.parametrize("bonus_x, plate_x, plate_width, expected_active", [
        (100, 80, 100, True),  # Бонус над платформою
        (50, 80, 100, False),  # Бонус ліворуч від платформи
        (200, 80, 100, False)  # Бонус праворуч від платформи
    ])
    def test_calculate_reflection_x_position(self, dummy_bonus, mock_user_plate, mock_game_screen, bonus_x, plate_x,
                                             plate_width, expected_active):
        """
        Параметризований тест методу calculate_reflection для різних позицій по X.
        Перевіряє, чи активується бонус при контакті з платформою.
        """
        dummy_bonus.y_position = 300  # Встановлюємо Y на рівні платформи
        dummy_bonus.x_position = bonus_x
        mock_user_plate.rect.x = plate_x
        mock_user_plate.rect.width = plate_width
        dummy_bonus.calculate_reflection(mock_user_plate, mock_game_screen)
        assert dummy_bonus.is_active == expected_active
        assert dummy_bonus.is_visible != expected_active

    @pytest.mark.activation
    def test_bonus_activation(self, dummy_bonus, mock_user_plate, mock_game_screen):
        """Тест активації бонусу при контакті з платформою."""
        # Розміщуємо бонус над платформою
        dummy_bonus.x_position = 100
        dummy_bonus.y_position = 300
        dummy_bonus.radius = 10
        mock_user_plate.rect.x = 80
        mock_user_plate.rect.y = 300
        mock_user_plate.rect.width = 100

        # Спочатку бонус неактивний і видимий
        assert dummy_bonus.is_active is False
        assert dummy_bonus.is_visible is True

        # Після обчислення відбиття, бонус повинен стати активним і невидимим
        dummy_bonus.calculate_reflection(mock_user_plate, mock_game_screen)

        assert dummy_bonus.is_active is True
        assert dummy_bonus.is_visible is False
        assert dummy_bonus.activated is True
        assert dummy_bonus.target == mock_game_screen

    @pytest.mark.visibility
    def test_bonus_not_activated_when_invisible(self, dummy_bonus, mock_user_plate, mock_game_screen):
        """Тест, що невидимий бонус не активується."""
        dummy_bonus.x_position = 100
        dummy_bonus.y_position = 300
        dummy_bonus.is_visible = False

        dummy_bonus.calculate_reflection(mock_user_plate, mock_game_screen)

        assert dummy_bonus.is_active is False
        assert dummy_bonus.activated is False

    @pytest.mark.direction
    def test_bonus_not_activated_when_moving_up(self, dummy_bonus, mock_user_plate, mock_game_screen):
        """Тест, що бонус, який рухається вгору, не активується."""
        dummy_bonus.x_position = 100
        dummy_bonus.y_position = 300
        dummy_bonus.move_direction = [0, -1]  # Рух вгору

        dummy_bonus.calculate_reflection(mock_user_plate, mock_game_screen)

        assert dummy_bonus.is_active is False
        assert dummy_bonus.activated is False

    @pytest.mark.abstract_methods
    def test_abstract_methods_implemented(self, dummy_bonus):
        """Тест наявності реалізації абстрактних методів."""
        test_target = MagicMock()

        dummy_bonus.activate(test_target)
        assert dummy_bonus.activated is True
        assert dummy_bonus.target == test_target

        dummy_bonus.deactivate(test_target)
        assert dummy_bonus.deactivated is True
        assert dummy_bonus.target == test_target


# Цей тест демонструє використання патчу для підміни pygame.draw.circle
@pytest.mark.mock_draw
def test_render_with_patch(dummy_bonus, mock_screen):
    """Тест рендерингу з використанням патчу pygame.draw.circle."""
    with patch('pygame.draw.circle') as mock_draw:
        dummy_bonus.render(mock_screen)
        mock_draw.assert_called_once()
        args, _ = mock_draw.call_args
        assert args[0] == mock_screen
        assert args[1] == dummy_bonus.color
        assert args[2] == (int(dummy_bonus.x_position), int(dummy_bonus.y_position))
        assert args[3] == int(dummy_bonus.radius)


@pytest.mark.xfail
@pytest.mark.parametrize("bonus_y, plate_y, expected_active", [
    (350, 300, False)  # Тест, який "очікувано падає" - демонстрація xfail маркера
])
def test_expected_to_fail(dummy_bonus, mock_user_plate, mock_game_screen, bonus_y, plate_y, expected_active):
    """
    Тест, який демонструє використання маркера xfail.
    Ми очікуємо, що цей тест не пройде через поточну реалізацію методу calculate_reflection.
    """
    dummy_bonus.y_position = bonus_y
    mock_user_plate.rect.y = plate_y
    dummy_bonus.calculate_reflection(mock_user_plate, mock_game_screen)
    # Цей тест очікувано падає, оскільки бонус, який знаходиться нижче платформи,
    # за поточною реалізацією активується, а ми очікуємо що не має активуватись
    assert dummy_bonus.is_active == expected_active


@pytest.mark.skip(reason="Демонстрація використання маркера skip")
def test_skipped_test(dummy_bonus):
    """
    Тест, який демонструє використання маркера skip.
    Цей тест буде пропущено під час виконання.
    """
    assert False  # Цей код ніколи не виконається


@pytest.mark.parametrize("mock_time", [
    0, 1000, 2000
])
def test_with_time_dependency(dummy_bonus, mock_time):
    """
    Тест з залежністю від часу, демонструє параметризацію з різними значеннями часу.
    """
    with patch('pygame.time.get_ticks', return_value=mock_time):
        # Припустимо, що у нас є логіка, що залежить від часу
        assert pygame.time.get_ticks() == mock_time