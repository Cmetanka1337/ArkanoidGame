import pygame
import random
from Models.Bonus import BonusObject
from Views.Abstract_classes.AbstractStaticObject import AbstractStaticObject
from Views.LevelPlate import LevelPlateObject

class LevelManager:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.blocks = []

    def load_level(self, level):
        self.blocks.clear()
        if level == 1:
            self.generate_rhombus()

    def generate_rhombus(self):
        block_width = 50
        block_height = 20
        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
        center_x = self.screen_width // 2
        center_y = self.screen_height // 4

        rows = 5
        for row in range(rows):
            for col in range(-row, row + 1):
                x = center_x + col * (block_width + 5)
                y = center_y + row * (block_height + 5)
                color = pygame.Color(*random.choice(colors))
                block = LevelPlateObject(
                    hit_points=3,
                    plate_type='standard',
                    is_breakable=True,
                    x_position=x,
                    y_position=y,
                    height=block_height,
                    width=block_width,
                    color=color
                )
                self.blocks.append(block)

        for row in range(rows - 1, -1, -1):
            for col in range(-row, row + 1):
                x = center_x + col * (block_width + 5)
                y = center_y + (rows * 2 - row - 2) * (block_height + 5)
                color = pygame.Color(*random.choice(colors))
                block = LevelPlateObject(
                    hit_points=3,
                    plate_type='standard',
                    is_breakable=True,
                    x_position=x,
                    y_position=y,
                    height=block_height,
                    width=block_width,
                    color=color
                )
                self.blocks.append(block)

        # Додаємо вертикальні лінії з боків
        side_blocks = 10
        for i in range(side_blocks):
            for side in [-1, 1]:
                x = center_x + side * (rows + 1) * (block_width + 5)
                y = center_y + i * (block_height + 5)
                color = pygame.Color(*random.choice(colors))
                block = LevelPlateObject(
                    hit_points=3,
                    plate_type='standard',
                    is_breakable=True,
                    x_position=x,
                    y_position=y,
                    height=block_height,
                    width=block_width,
                    color=color
                )
                self.blocks.append(block)

    def render(self, screen):
        for block in self.blocks:
            block.render(screen)
