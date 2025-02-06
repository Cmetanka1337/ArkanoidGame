from Controllers.SceneModule import SceneObject

class Game:

    end_score: int = 0
    background_color: str
    language: str
    volume: float

    def start(self):
        pass

    def level_selection(self):
        pass

    def finish_game(self):
        pass

    def draw_scene(self) -> SceneObject:
        pass

    def restart(self):
        pass

    def close(self):
        pass

    def change_background(self):
        pass

    def change_language(self):
        pass

    def change_volume(self):
        pass
