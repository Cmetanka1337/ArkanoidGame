from Views.Abstract_classes.AbstractObject import AbstractObject


class BonusObject:
    bonus_effect: str
    is_caught: bool
    duration: int

    def __init__(self, bonus_effect: str, is_caught: bool, duration: int):
        self.bonus_effect = bonus_effect
        self.is_caught = is_caught
        self.duration = duration

    def activate(self, target: AbstractObject):
        pass

    def deactivate(self, target: AbstractObject):
        pass