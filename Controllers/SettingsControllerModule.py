import pygame
from pygame_gui import UIManager

from Models.LocalizedStringEnglish import LocalizedStringEnglish
from Models.LocalizedStrings import LocalizedStrings


class SettingsController:

    def __init__(self):
        self.background_color = "blue_theme.json"
        self.language = LocalizedStringEnglish()
        self.volume = 0.15

    def change_background(self, window_surface, color) -> UIManager:
        manager = UIManager(window_surface.get_size(), f"../Assets/{color}")
        return manager

    def change_language(self, language: LocalizedStrings):
        from Controllers import GameModule
        GameModule.selected_language = language
        self.language = language

    def change_volume(self, volume: float):
        if volume < 0:
            volume = 0
        if volume > 1:
            volume = 1
        pygame.mixer.music.set_volume(volume)
        self.volume = volume

    def get_background(self):
        return self.background_color

    def get_language(self):
        return self.language

    def get_volume(self):
        return self.volume