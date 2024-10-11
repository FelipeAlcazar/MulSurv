import pygame

class Weapon:
    predefined_weapons = {
        "Gun": {"sound_path": 'assets/sounds/gunShot.mp3', "shoot_delay": 1000, "volume": 0.6}
    }

    def __init__(self, name, sound_path=None, shoot_delay=None, volume=1.0):
        if name in self.predefined_weapons:
            weapon_info = self.predefined_weapons[name]
            self.name = name
            self.sound_path = weapon_info["sound_path"]
            self.shoot_delay = weapon_info["shoot_delay"]
            self.volume = weapon_info["volume"]
        else:
            self.name = name
            self.sound_path = sound_path
            self.shoot_delay = shoot_delay
            self.volume = volume

        self.sound = pygame.mixer.Sound(self.sound_path)
        self.sound.set_volume(self.volume)

    def play_sound(self):
        self.sound.play()