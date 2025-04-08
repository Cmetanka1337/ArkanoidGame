import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
import pygame
from unittest.mock import MagicMock, patch
from Views.Abstract_classes.AbstractBonusObject import AbstractBonusObject
from Views.Ball import BallObject
from Views.Screens.GameScreenModule import GameScreen
from Views.AdditionalBallsBonus import AdditionalBallsBonus


@pytest.fixture
def balls_bonus():
    """
    Базова фікстура, яка створює екземпляр бонусу додаткових м'ячів для тестування.
    """
    return AdditionalBallsBonus(
        x_position=100.0,
        y_position=200.0,
        height=20.0,
        width=20.0,
        color=pygame.Color(0, 255, 0),  # Зелений колір для бонусу
        speed=5.0,
        move_direction=[0, 1],
        radius=10.0,
        is_active=False,
        balls_number=3.0  # Створюємо 3 додаткових м'ячі
    )


@pytest.fixture
def mock_game_screen():
    """
    Фікстура, яка створює макет ігрового екрану.
    """
    screen = MagicMock(spec=GameScreen)
    screen.balls = []  # Початково немає м'ячів
    return screen


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


@pytest.fixture
def mock_screen():
    """
    Фікстура, яка створює макет екрану для тестування рендерингу.
    """
    return MagicMock()


class TestAdditionalBallsBonus:

    @pytest.mark.initialization
    def test_initialization(self, balls_bonus):
        """Тест коректної ініціалізації бонусу додаткових м'ячів."""
        assert balls_bonus.x_position == 100.0
        assert balls_bonus.y_position == 200.0
        assert balls_bonus.height == 20.0
        assert balls_bonus.width == 20.0
        assert balls_bonus.color == pygame.Color(0, 255, 0)
        assert balls_bonus.is_visible is True
        assert balls_bonus.speed == 5.0
        assert balls_bonus.move_direction == [0, 1]
        assert balls_bonus.radius == 10.0
        assert balls_bonus.is_active is False
        assert balls_bonus.balls_number == 3.0

    @pytest.mark.inheritance
    def test_inheritance(self, balls_bonus):
        """Тест, що перевіряє чи клас дійсно успадковує AbstractBonusObject."""
        assert isinstance(balls_bonus, AbstractBonusObject)

    @pytest.mark.activation
    def test_activate(self, balls_bonus, mock_game_screen):
        """Тест активації бонусу додаткових м'ячів."""
        # До активації немає м'ячів на екрані
        assert len(mock_game_screen.balls) == 0
        assert balls_bonus.is_active is False

        # Активуємо бонус
        balls_bonus.activate(mock_game_screen)

        # Після активації бонус має бути активним
        assert balls_bonus.is_active is True

        # М'ячі мають бути додані до екрану
        assert len(mock_game_screen.balls) == 3  # 3 нових м'ячі

        # Перевірка створених м'ячів
        for i, ball in enumerate(mock_game_screen.balls):
            assert isinstance(ball, BallObject)
            assert ball.x_position == 200 + i * 20
            assert ball.y_position == 100
            assert ball.color == pygame.Color(255, 0, 0)  # Червоний м'яч
            assert ball.radius == 5
            assert ball.move_direction == [1, 1]
            assert ball.is_visible is True

    @pytest.mark.activation
    @pytest.mark.parametrize("balls_number", [1.0, 2.0, 5.0])
    def test_activate_different_number_of_balls(self, balls_bonus, mock_game_screen, balls_number):
        """Параметризований тест активації бонусу з різною кількістю м'ячів."""
        balls_bonus.balls_number = balls_number

        # Активуємо бонус
        balls_bonus.activate(mock_game_screen)

        # Перевіряємо, що створена правильна кількість м'ячів
        assert len(mock_game_screen.balls) == int(balls_number)

    @pytest.mark.activation
    @pytest.mark.parametrize("initial_balls", [0, 1, 3])
    def test_activate_with_existing_balls(self, balls_bonus, mock_game_screen, initial_balls):
        """Тест активації бонусу, коли на екрані вже є м'ячі."""
        # Додаємо початкові м'ячі до екрану
        for i in range(initial_balls):
            mock_game_screen.balls.append(
                BallObject(150, 150, 10, 10, pygame.Color(0, 0, 255), 5, [1, 1], 5, True)
            )

        # Активуємо бонус
        balls_bonus.activate(mock_game_screen)

        # Після активації має бути початкова кількість + додаткові м'ячі
        assert len(mock_game_screen.balls) == initial_balls + int(balls_bonus.balls_number)

    @pytest.mark.deactivation
    def test_deactivate(self, balls_bonus, mock_game_screen):
        """Тест деактивації бонусу."""
        # В поточній реалізації метод deactivate нічого не робить
        # Але ми все одно тестуємо його для повноти тестування
        balls_bonus.deactivate(mock_game_screen)
        # Перевіряємо, що метод просто виконується без помилок
        assert True  # Тест просто підтверджує, що метод виконується

    @pytest.mark.rendering
    def test_render(self, balls_bonus, mock_screen):
        """Тест методу render, який малює бонус на екрані."""
        with patch('pygame.draw.circle') as mock_draw:
            balls_bonus.render(mock_screen)
            mock_draw.assert_called_once_with(
                mock_screen,
                balls_bonus.color,
                (int(balls_bonus.x_position), int(balls_bonus.y_position)),
                int(balls_bonus.radius)
            )

    @pytest.mark.collision
    def test_calculate_reflection(self, balls_bonus, mock_user_plate, mock_game_screen):
        """Тест методу calculate_reflection успадкованого від AbstractBonusObject."""
        # Розміщуємо бонус над платформою
        balls_bonus.x_position = 100
        balls_bonus.y_position = 300
        mock_user_plate.rect.x = 80
        mock_user_plate.rect.y = 300

        # Спочатку бонус неактивний
        assert balls_bonus.is_active is False
        assert len(mock_game_screen.balls) == 0

        # Перевіряємо, що бонус активується при контакті з платформою
        with patch.object(balls_bonus, 'activate') as mock_activate:
            balls_bonus.calculate_reflection(mock_user_plate, mock_game_screen)
            mock_activate.assert_called_once_with(mock_game_screen)
            assert balls_bonus.is_visible is False

    @pytest.mark.movement
    @pytest.mark.parametrize("direction, expected_pos", [
        ([1, 0], (105.0, 200.0)),  # Рух вправо
        ([0, 1], (100.0, 205.0)),  # Рух вниз
        ([-1, 0], (95.0, 200.0)),  # Рух вліво
        ([0, -1], (100.0, 195.0))  # Рух вгору
    ])
    def test_update_position(self, balls_bonus, direction, expected_pos):
        """Параметризований тест оновлення позиції бонусу."""
        balls_bonus.move_direction = direction
        balls_bonus.update_position()
        assert (balls_bonus.x_position, balls_bonus.y_position) == expected_pos

    @pytest.mark.movement
    def test_move_to(self, balls_bonus):
        """Тест методу move_to успадкованого від AbstractMovableObject."""
        balls_bonus.move_to(2.0, -1.0)
        assert balls_bonus.move_direction == [2.0, -1.0]
        assert balls_bonus.x_position == 110.0  # 100 + 5*2
        assert balls_bonus.y_position == 195.0  # 200 + 5*(-1)

    @pytest.mark.visibility
    def test_visibility_after_activation(self, balls_bonus, mock_game_screen):
        """Тест, що перевіряє видимість бонусу після активації."""
        # Початково бонус видимий
        assert balls_bonus.is_visible is True

        # Активуємо бонус через calculate_reflection
        with patch.object(balls_bonus, 'activate') as mock_activate:
            # Імітуємо контакт з платформою для активації
            mock_user_plate = MagicMock()
            mock_user_plate.rect = MagicMock()
            mock_user_plate.rect.x = 80
            mock_user_plate.rect.y = 300
            mock_user_plate.rect.width = 100

            balls_bonus.x_position = 100
            balls_bonus.y_position = 290
            balls_bonus.calculate_reflection(mock_user_plate, mock_game_screen)

            # Бонус має стати невидимим після активації
            assert balls_bonus.is_visible is False
            mock_activate.assert_called_once_with(mock_game_screen)

    @pytest.mark.skip(reason="Демонстрація використання маркера skip")
    def test_skipped_test(self):
        """
        Тест з маркером skip, який буде пропущено.
        """
        assert False  # Ніколи не виконається

    @pytest.mark.xfail(reason="Демонстрація використання маркера xfail")
    def test_expected_to_fail(self):
        """
        Тест з маркером xfail - очікувано падаючий тест.
        """
        # Цей тест очікувано падає, оскільки перевіряє неіснуючу поведінку
        assert 1 == 2  # Завжди падає