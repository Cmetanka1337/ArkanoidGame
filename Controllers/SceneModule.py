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
