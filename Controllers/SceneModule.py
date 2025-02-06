from Models.Bonus import BonusObject
from Views.Ball import BallObject
from Views.LevelPlate import LevelPlateObject


class SceneObject:
    score_label: str # some label type from UI framework
    lives_label: str # some label type from UI framework
    wall_plates: [] # there is no WallPlateObject in the system right now
    level_plates: [LevelPlateObject]
    ball: BallObject
    scene_size: (float, float)
    buttons: [] # some buttons type from UI framework

    def update_scene(self):
        pass

    def remove_plate(self):
        pass

    def move_user_plate(self):
        pass

    def apply_bonus(self, bonus: BonusObject):
        pass

    def move_ball(self, x: float, y: float):
        pass

    def did_tap_button(self, button: []):
        pass

    def draw_ball_at(self, x: float, y: float):
        pass

    def show_end_game_screen(self):
        pass

    def reset_level(self):
        pass