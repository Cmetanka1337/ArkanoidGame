from Models.LocalizedStringEnglish import LocalizedStringEnglish
from Models.LocalizedStrings import LocalizedStrings


class SettingsController:

    def __init__(self):
        self.background_color = "Light"
        self.language = LocalizedStringEnglish()
        self.volume = 0.5

    def change_background(self, color):
        self.background_color = color

    def change_language(self, language: LocalizedStrings):
        self.language = language

    def change_volume(self, volume):
        self.volume = volume

    def get_background(self):
        return self.background_color

    def get_language(self):
        return self.language

    def get_volume(self):
        return self.volume