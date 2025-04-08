import pygame
from Views.Abstract_classes.AbstractMovableObject import AbstractMovableObject
from Views.Scene import SceneObject
class BallObject(AbstractMovableObject):

    speed: float
    move_direction: list
    radius: float
    is_visible: bool

    def __init__(self, x_position: float, y_position: float,
                 height: float, width: float,
                 color: pygame.Color,
                 speed: float, move_direction: list, radius: float, is_visible: bool):
        super().__init__(x_position, y_position, height, width, color, True)
        self.speed = speed
        self.move_direction = move_direction
        self.radius = radius
        self.is_visible = is_visible

    def render(self, screen):
        if self.is_visible:
            pygame.draw.circle(
                screen,
                self.color,
                (int(self.x_position), int(self.y_position)),
                int(self.radius)
            )

    def move_to(self, x: float, y: float):
        # Встановлюємо напрямок руху,
        # а потім рухаємо м'яч, змінюючи координати x та y
        self.move_direction[0] = x
        self.move_direction[1] = y
        self.x_position += self.speed * self.move_direction[0]
        self.y_position += self.speed * self.move_direction[1]

    def update_position(self, target):
        """
        Оновлює позицію м'яча згідно з поточним напрямком руху та швидкістю.
        """
        self.x_position += self.speed * self.move_direction[0]
        self.y_position += self.speed * self.move_direction[1]

        if self.y_position - self.radius > SceneObject.height:
            self.is_visible = False
    # метод, який обчислює траекторії руху після зіткнення з будь - яким обʼєктом.

    def calculate_reflection(self,user_plate,level_manager):
        #логіка відбиття м'яча від країв екрану
        if self.x_position < self.radius or self.x_position > SceneObject.width - self.radius:
            self.move_direction[0] *=-1

        if self.y_position < self.radius:
            self.move_direction[1] *= -1

        # Відбиття від платформи гравця (якщо м'яч рухається вниз)
        if self.move_direction[1] > 0:
            if self.y_position + self.radius >= user_plate.rect.y:
                if (user_plate.rect.x <= self.x_position <=
                        user_plate.rect.x + user_plate.rect.width):
                    self.move_direction[1] *= -1

        # Відбиття від блоків рівня
        for plate in level_manager.blocks:
            if plate.is_visible:
                plate_left = plate.rect.x
                plate_right = plate.rect.x + plate.rect.width
                plate_top = plate.rect.y
                plate_bottom = plate.rect.y + plate.rect.height

                if (plate_left - self.radius
                        <= self.x_position <= plate_right + self.radius and
                        plate_top - self.radius
                        <= self.y_position <= plate_bottom + self.radius):

                    overlap_x = min(
                        abs(self.x_position - plate_left),
                        abs(self.x_position - plate_right)
                    )
                    overlap_y = min(
                        abs(self.y_position - plate_top),
                        abs(self.y_position - plate_bottom)
                    )

                    if overlap_x > overlap_y:
                        self.move_direction[1] *= -1
                    else:
                        self.move_direction[0] *= -1

                    if plate.is_breakable:
                        plate.decrease_hit_points()
                        plate.update_state()

    def reset_position(self):
        """
        Переміщує м'яч у центр по X і трохи вище нижнього краю по Y.
        """
        self.x_position = SceneObject.width // 2
        self.y_position = SceneObject.height - 50
