"""Управление звуками и музыкой"""

import pygame
import os


class SoundManager:
    """Класс для управления звуковыми эффектами и музыкой"""

    def __init__(self):
        try:
            pygame.mixer.init()
        except:
            print("Предупреждение: Не удалось инициализировать звуковую систему")

        self.sounds = {}
        self.music_playing = False
        self.sound_enabled = True
        self.music_enabled = True
        self.load_sounds()

    def load_sounds(self):
        """Загрузка звуковых файлов"""
        sound_files = {
            'move': 'move.wav',
            'rotate': 'rotate.wav',
            'drop': 'drop.wav',
            'clear': 'clear.wav',
            'tetris': 'tetris.wav',
            'game_over': 'game_over.wav',
            'level_up': 'level_up.wav'
        }

        for name, filename in sound_files.items():
            try:
                path = os.path.join('assets', 'sounds', filename)
                if os.path.exists(path):
                    self.sounds[name] = pygame.mixer.Sound(path)
                else:
                    self.sounds[name] = None
            except:
                self.sounds[name] = None

    def play_sound(self, sound_name):
        """Воспроизведение звука"""
        if self.sound_enabled and sound_name in self.sounds:
            sound = self.sounds[sound_name]
            if sound:
                try:
                    sound.play()
                except:
                    pass

    def play_music(self):
        """Воспроизведение фоновой музыки"""
        if self.music_enabled:
            try:
                music_path = os.path.join('assets', 'music', 'background.mp3')
                if os.path.exists(music_path):
                    pygame.mixer.music.load(music_path)
                    pygame.mixer.music.set_volume(0.5)
                    pygame.mixer.music.play(-1)
                    self.music_playing = True
                else:
                    print("Музыкальный файл не найден. Игра без музыки.")
            except Exception as e:
                print(f"Не удалось воспроизвести музыку: {e}")

    def stop_music(self):
        """Остановка музыки"""
        try:
            pygame.mixer.music.stop()
            self.music_playing = False
        except:
            pass

    def toggle_sound(self):
        """Включение/выключение звуков"""
        self.sound_enabled = not self.sound_enabled

    def toggle_music(self):
        """Включение/выключение музыки"""
        self.music_enabled = not self.music_enabled
        if self.music_enabled:
            self.play_music()
        else:
            self.stop_music()