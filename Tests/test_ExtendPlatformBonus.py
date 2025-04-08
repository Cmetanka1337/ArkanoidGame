import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
import pygame
from unittest.mock import MagicMock, patch
from Views.Abstract_classes.AbstractBonusObject import AbstractBonusObject
from Views.UserPlate import UserPlateObject
from Views.ExtendPlatformBonus import ExtendPlatformBonus


@pytest.fixture
def platform_bonus():
    """
    Базова фікстура, яка створює екземпляр бонусу розширення платформи для тестування.
    """
    return ExtendPlatformBonus(
        x_position=100.0,
        y_position=200.0,
        height=20.0,
        width=20.0,
        color=pygame.Color(0, 0, 255),  # Синій колір для бонусу
        speed=5.0,
        move_direction=[0, 1],
        radius=10.0,
        is_active=False,
        duration=3.0,  # Тривалість дії бонусу 3 секунди
        extend_size=300.0  # Розширення платформи до 300 пікселів
    )


@pytest.fixture
def mock_user_plate():
    """
    Фікстура, яка створює макет платформи користувача.
    """
    plate = MagicMock(spec=UserPlateObject)
    plate.rect = MagicMock()
    plate.rect.x = 80
    plate.rect.y = 300
    plate.rect.width = 200  # Початковий розмір платформи
    return plate


@pytest.fixture
def mock_game_screen():
    """
    Фікстура, яка створює макет ігрового екрану.
    """
    return MagicMock()


@pytest.fixture
def mock_screen():
    """
    Фікстура, яка створює макет екрану для тестування рендерингу.
    """
    return MagicMock()


class TestExtendPlatformBonus:

    @pytest.mark.initialization
    def test_initialization(self, platform_bonus):
        """Тест коректної ініціалізації бонусу розширення платформи."""
        assert platform_bonus.x_position == 100.0
        assert platform_bonus.y_position == 200.0
        assert platform_bonus.height == 20.0
        assert platform_bonus.width == 20.0
        assert platform_bonus.color == pygame.Color(0, 0, 255)
        assert platform_bonus.is_visible is True
        assert platform_bonus.speed == 5.0
        assert platform_bonus.move_direction == [0, 1]
        assert platform_bonus.radius == 10.0
        assert platform_bonus.is_active is False
        assert platform_bonus.duration == 3.0
        assert platform_bonus.extend_size == 300.0
        assert platform_bonus.start_time is None

    @pytest.mark.inheritance
    def test_inheritance(self, platform_bonus):
        """Тест, що перевіряє чи клас дійсно успадковує AbstractBonusObject."""
        assert isinstance(platform_bonus, AbstractBonusObject)

    @pytest.mark.activation
    def test_activate(self, platform_bonus, mock_user_plate):
        """Тест активації бонусу розширення платформи."""
        with patch('pygame.time.get_ticks', return_value=1000):
            platform_bonus.activate(mock_user_plate)

            # Перевіряємо, що бонус активований
            assert platform_bonus.is_active is True
            assert platform_bonus.start_time == 1000

            # Перевіряємо, що метод resize викликався з правильним значенням
            mock_user_plate.resize.assert_called_once_with(platform_bonus.extend_size)

    @pytest.mark.deactivation
    def test_deactivate(self, platform_bonus, mock_user_plate):
        """Тест деактивації бонусу розширення платформи."""
        # Активуємо бонус перед деактивацією
        platform_bonus.is_active = True
        platform_bonus.start_time = 1000

        # Деактивуємо бонус
        platform_bonus.deactivate(mock_user_plate)

        # Перевіряємо, що бонус деактивований
        assert platform_bonus.is_active is False

        # Перевіряємо, що метод resize викликався з стандартним значенням
        mock_user_plate.resize.assert_called_once_with(200)

    @pytest.mark.update
    @pytest.mark.parametrize("current_time, expected_active", [
        (2000, True),  # Пройшло 1 секунда з активації - бонус ще активний
        (4000, True),  # Пройшло 3 секунди з активації - бонус ще активний
        (4001, False)  # Пройшло більше 3 секунд - бонус має деактивуватися
    ])
    def test_update(self, platform_bonus, mock_user_plate, current_time, expected_active):
        """Параметризований тест методу update з різними проміжками часу."""
        # Встановлюємо початковий час активації
        with patch('pygame.time.get_ticks', return_value=1000):
            platform_bonus.activate(mock_user_plate)

        # Скидаємо лічильник викликів перед новим тестом
        mock_user_plate.resize.reset_mock()

        # Тестуємо оновлення з різними поточними часами
        with patch('pygame.time.get_ticks', return_value=current_time):
            platform_bonus.update(mock_user_plate)

            assert platform_bonus.is_active is expected_active

            # Якщо бонус деактивувався, перевіряємо виклик resize
            if not expected_active:
                mock_user_plate.resize.assert_called_once_with(200)
            else:
                mock_user_plate.resize.assert_not_called()

    @pytest.mark.rendering
    def test_render(self, platform_bonus, mock_screen):
        """Тест методу render, який малює бонус на екрані."""
        with patch('pygame.draw.circle') as mock_draw:
            platform_bonus.render(mock_screen)
            mock_draw.assert_called_once_with(
                mock_screen,
                platform_bonus.color,
                (int(platform_bonus.x_position), int(platform_bonus.y_position)),
                int(platform_bonus.radius)
            )

    @pytest.mark.collision
    def test_calculate_reflection(self, platform_bonus, mock_user_plate, mock_game_screen):
        """Тест методу calculate_reflection."""
        # Розміщуємо бонус над платформою для тестування зіткнення
        platform_bonus.x_position = 100
        platform_bonus.y_position = 290  # Прямо над платформою

        # Початково бонус неактивний і видимий
        assert platform_bonus.is_active is False
        assert platform_bonus.is_visible is True

        # Перехоплюємо виклик activate для тестування calculate_reflection
        with patch.object(platform_bonus, 'activate') as mock_activate:
            platform_bonus.calculate_reflection(mock_user_plate, mock_game_screen)

            # Бонус має стати активним і невидимим
            assert platform_bonus.is_active is True
            assert platform_bonus.is_visible is False

            # Метод activate має викликатися з платформою користувача
            mock_activate.assert_called_once_with(mock_user_plate)

    @pytest.mark.collision
    @pytest.mark.parametrize("bonus_x, plate_x, plate_width, expected_active", [
        (100, 80, 100, True),  # Бонус над платформою
        (50, 80, 100, False),  # Бонус ліворуч від платформи
        (200, 80, 100, False)  # Бонус праворуч від платформи
    ])
    def test_calculate_reflection_x_position(self, platform_bonus, mock_user_plate, mock_game_screen,
                                             bonus_x, plate_x, plate_width, expected_active):
        """Параметризований тест методу calculate_reflection для різних позицій по X."""
        platform_bonus.y_position = 300  # На рівні верху платформи
        platform_bonus.x_position = bonus_x
        mock_user_plate.rect.x = plate_x
        mock_user_plate.rect.width = plate_width

        # Перехоплюємо виклик activate для чистоти тесту
        with patch.object(platform_bonus, 'activate'):
            platform_bonus.calculate_reflection(mock_user_plate, mock_game_screen)

            assert platform_bonus.is_active is expected_active
            assert platform_bonus.is_visible is not expected_active

    @pytest.mark.collision
    @pytest.mark.parametrize("bonus_y, plate_y, expected_active", [
        (290, 300, True),  # Бонус торкається верхньої межі платформи
        (250, 300, False)  # Бонус вище платформи
    ])
    def test_calculate_reflection_y_position(self, platform_bonus, mock_user_plate, mock_game_screen,
                                             bonus_y, plate_y, expected_active):
        """Параметризований тест методу calculate_reflection для різних позицій по Y."""
        platform_bonus.x_position = 100  # Над платформою по X
        platform_bonus.y_position = bonus_y
        mock_user_plate.rect.y = plate_y

        # Перехоплюємо виклик activate для чистоти тесту
        with patch.object(platform_bonus, 'activate'):
            platform_bonus.calculate_reflection(mock_user_plate, mock_game_screen)

            assert platform_bonus.is_active is expected_active
            assert platform_bonus.is_visible is not expected_active

    @pytest.mark.visibility
    def test_bonus_not_activated_when_invisible(self, platform_bonus, mock_user_plate, mock_game_screen):
        """Тест, що невидимий бонус не активується."""
        platform_bonus.x_position = 100
        platform_bonus.y_position = 300
        platform_bonus.is_visible = False

        with patch.object(platform_bonus, 'activate') as mock_activate:
            platform_bonus.calculate_reflection(mock_user_plate, mock_game_screen)

            # Бонус не повинен активуватися
            assert platform_bonus.is_active is False
            mock_activate.assert_not_called()

    @pytest.mark.direction
    def test_bonus_not_activated_when_moving_up(self, platform_bonus, mock_user_plate, mock_game_screen):
        """Тест, що бонус, який рухається вгору, не активується."""
        platform_bonus.x_position = 100
        platform_bonus.y_position = 300
        platform_bonus.move_direction = [0, -1]  # Рух вгору

        with patch.object(platform_bonus, 'activate') as mock_activate:
            platform_bonus.calculate_reflection(mock_user_plate, mock_game_screen)

            # Бонус не повинен активуватися
            assert platform_bonus.is_active is False
            mock_activate.assert_not_called()

    @pytest.mark.timing
    def test_bonus_duration(self, platform_bonus, mock_user_plate):
        """Тест тривалості дії бонусу з симуляцією проходження часу."""
        # Встановлюємо початковий час
        with patch('pygame.time.get_ticks', return_value=1000):
            platform_bonus.activate(mock_user_plate)

        mock_user_plate.resize.reset_mock()

        # Перевіряємо стан після половини тривалості
        with patch('pygame.time.get_ticks', return_value=2500):  # 1000 + 1500 (1.5 секунди)
            platform_bonus.update(mock_user_plate)
            assert platform_bonus.is_active is True
            mock_user_plate.resize.assert_not_called()

        # Перевіряємо стан після повної тривалості
        with patch('pygame.time.get_ticks', return_value=4001):  # 1000 + 3001 (трохи більше 3 секунд)
            platform_bonus.update(mock_user_plate)
            assert platform_bonus.is_active is False
            mock_user_plate.resize.assert_called_once_with(200)

    @pytest.mark.parametrize("time_values", [
        [1000, 2000, 3000, 4000, 4001],  # Послідовність часів
    ])
    def test_bonus_lifecycle(self, platform_bonus, mock_user_plate, time_values):
        """Тест повного життєвого циклу бонусу."""
        # Початковий стан
        assert platform_bonus.is_active is False
        assert platform_bonus.start_time is None

        # Активуємо бонус
        with patch('pygame.time.get_ticks', return_value=time_values[0]):
            platform_bonus.activate(mock_user_plate)
            assert platform_bonus.is_active is True
            assert platform_bonus.start_time == time_values[0]

        # Перевіряємо, що бонус активний на проміжних часах
        for time in time_values[1:-1]:
            mock_user_plate.resize.reset_mock()
            with patch('pygame.time.get_ticks', return_value=time):
                platform_bonus.update(mock_user_plate)
                assert platform_bonus.is_active is True
                mock_user_plate.resize.assert_not_called()

        # Перевіряємо деактивацію після закінчення тривалості
        mock_user_plate.resize.reset_mock()
        with patch('pygame.time.get_ticks', return_value=time_values[-1]):
            platform_bonus.update(mock_user_plate)
            assert platform_bonus.is_active is False
            mock_user_plate.resize.assert_called_once_with(200)

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