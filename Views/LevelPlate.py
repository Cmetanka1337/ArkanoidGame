import pygame
from Models.Bonus import BonusObject
from Views.Abstract_classes.AbstractBonusObject import AbstractBonusObject
from Views.Abstract_classes.AbstractStaticObject import AbstractStaticObject

class LevelPlateObject(AbstractStaticObject):
    alpha_values = {3: 255, 2: 170, 1: 85}
    hit_points: int
    plate_type: str # standard plate or with a bonus, for example
    alpha:int
    def __init__(self,hit_points: int, plate_type: str, is_breakable: bool, x_position: float, y_position: float, height: float, width: float,
                 color: pygame.Color, is_visible=True, level_manager=None):
        super().__init__(is_breakable, x_position, y_position, height, width, color, is_visible)
        self.hit_points = hit_points
        self.plate_type = plate_type
        self.alpha = 255
        self.rect = pygame.Rect(x_position, y_position, width, height)
        self.color.a = self.alpha
        self.level_manager= level_manager
        self.active_bonuses = []
    def render(self, screen):
        """ Малює платформу, якщо вона видима """
        if self.is_visible:
            surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            surface.fill((self.color.r, self.color.g, self.color.b, self.alpha))
            screen.blit(surface, self.rect.topleft)

    def destroy_platform(self):
        """ Знищує платформу з гри """
        if self.level_manager:  # Переконайтесь, що level_manager існує
            self.level_manager.remove_block(self)

    def decrease_hit_points(self):
        """ Зменшує міцність платформи, робить її невидимою при руйнуванні """
        if self.is_breakable:
            self.hit_points -= 1
            if self.hit_points > 0:
                self.alpha = self.alpha_values.get(self.hit_points,50)
                self.color.a = self.alpha
            else:
                self.is_visible = False
                self.destroy_platform()
                print("Platform destroyed")

        if self.plate_type == 'bonus':
            bonus = self.spawn_bonus()
            # Переконайся, що self.active_bonuses існує та оновлюється
            if bonus:
                self.active_bonuses.append(bonus)  # Додаємо бонус у список
                print(f"Bonus {bonus} spawned and added to active bonuses")  # Дебаг
            self.is_visible = False

    def spawn_bonus(self) -> BonusObject:
        if self.plate_type == 'bonus':
            # Можна, наприклад, випадково вибирати бонус між ExtendPlatformBonus і AdditionalBallsBonus
            import random
            from Views.ExtendPlatformBonus import ExtendPlatformBonus
            from Views.AdditionalBallsBonus import AdditionalBallsBonus
            bonus_classes = [ExtendPlatformBonus, AdditionalBallsBonus]
            bonus_class = random.choice(bonus_classes)
            # Створимо бонус у центрі блоку, задаючи параметри (вони можуть бути налаштовані)
            if bonus_class == ExtendPlatformBonus:
                bonus = bonus_class(
                    x_position=self.rect.centerx,
                    y_position=self.rect.centery,
                    height=20,
                    width=20,
                    color=self.color,
                    speed=5,
                    move_direction=[0, 1],  # бонус падає вниз
                    radius=10,
                    is_active=False,
                    duration=10,  # бонус діятиме 10 секунд (для ExtendPlatformBonus)
                    extend_size=400  # приклад параметра для розширення платформи
                )
            else:
                bonus = bonus_class(
                    x_position=self.rect.centerx,
                    y_position=self.rect.centery,
                    height=20,
                    width=20,
                    color=self.color,
                    speed=5,
                    move_direction=[0, 1],  # бонус падає вниз
                    radius=10,
                    is_active=False,
                    balls_number = 2
                )

            return bonus

    def update_state(self):
        """ Плавне зникнення після руйнування"""
        if not self.is_visible and self.alpha > 0:
            self.alpha = max(self.alpha-10,0)

