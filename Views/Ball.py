from Views.Abstract_classes.AbstractMovableObject import AbstractMovableObject
from Views.Scene import SceneObject
class BallObject(AbstractMovableObject):

    speed: float
    move_direction: list #я змінив тип на список ,тому що кортеж незмінний тип
    radius: float

    def __init__(self, x_position: float, y_position: float,
                 height: float, width: float,
                 color: str,
                 speed: float, move_direction: (int, int), radius: float):
        super().__init__(x_position, y_position, height, width, color, True)
        self.speed = speed
        self.move_direction = move_direction
        self.radius = radius

    def render(self):
        pass

    def move_to(self, x: float, y: float)
        #встановлюємо напрямок руху а потім рухаємо в тому напрямку мяч змінюючи координати х та у
        self.move_direction[0] = x
        self.move_direction[1] = y
        self.x_position += self.speed *self.move_direction[0]
        self.y_position += self.speed *self.move_direction[1]

    # метод, який обчислює траекторії руху після зіткнення з будь - яким обʼєктом.
    def calculate_reflection(self):
        #логіка відбиття м'яча від країв екрану
        if self.x_position < self.radius or self.x_position > SceneObject.width - self.radius:
            self.move_direction[0] *=-1
        if self.y_position < self.radius:
            self.move_direction[1] *=-1

    #мяч стає посередині екрану по х та знизу по у
    def reset_position(self):
        self.x_position = SceneObject.width // 2
        self.y_position = SceneObject.height - 50


