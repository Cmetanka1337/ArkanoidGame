import pygame
from Views.Abstract_classes.AbstractMovableObject import AbstractMovableObject
from Views.Scene import SceneObject
class BallObject(AbstractMovableObject):

    speed: float
    move_direction: list #я змінив тип на список ,тому що кортеж незмінний тип
    radius: float

    def __init__(self, x_position: float, y_position: float,
                 height: float, width: float,
                 color: pygame.Color,
                 speed: float, move_direction: list, radius: float):
        super().__init__(x_position, y_position, height, width, color, True)
        self.speed = speed
        self.move_direction = move_direction
        self.radius = radius


    def render(self,screen):
        pygame.draw.circle(screen, self.color,(int(self.x_position), int(self.y_position)),int(self.radius))

    def move_to(self, x: float, y: float):
        #встановлюємо напрямок руху а потім рухаємо в тому напрямку мяч змінюючи координати х та у
        self.move_direction[0] = x
        self.move_direction[1] = y
        self.x_position += self.speed *self.move_direction[0]
        self.y_position += self.speed *self.move_direction[1]

    def update_position(self):
        """
        Оновлює позицію м'яча згідно з поточним напрямком руху та швидкістю.
        """
        self.x_position += self.speed * self.move_direction[0]
        self.y_position += self.speed * self.move_direction[1]

    # метод, який обчислює траекторії руху після зіткнення з будь - яким обʼєктом.
    def calculate_reflection(self,user_plate):
        #логіка відбиття м'яча від країв екрану
        if self.x_position < self.radius or self.x_position > SceneObject.width - self.radius:
            self.move_direction[0] *=-1

        if self.y_position < self.radius:
            self.move_direction[1] *=-1
        # Логіка обробки зіткнення з платформою
        # Перевіряємо, чи мяч рухається вниз
        if self.move_direction[1] > 0:
            # Перевірка, чи досяг мяч верхньої межі платформи
            if self.y_position + self.radius >= user_plate.rect.y:
                # Перевірка, чи знаходиться мяч по осі X в межах платформи
                if user_plate.rect.x <= self.x_position <= user_plate.rect.x + user_plate.rect.width:
                    # Відбиваємо мяч від платформи (змінюємо вертикальну складову руху)
                    self.move_direction[1] *= -1

    #мяч стає посередині екрану по х та знизу по у
    def reset_position(self):
        self.x_position = SceneObject.width // 2
        self.y_position = SceneObject.height - 50




