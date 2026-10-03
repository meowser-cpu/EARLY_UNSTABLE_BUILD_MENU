import pygame
import numpy as np

class Synth:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.init()
        self.sample_rate = 44100
        self.freq = 440
        self.volume = 50
        self.duration = 500
        self.wave_type = 'sine'
        
    def play(self):
        duration_seconds = self.duration / 1000.0
        num_samples = int(duration_seconds * self.sample_rate)
        time_array = np.linspace(0, duration_seconds, num_samples, False)
        
        if self.wave_type == 'sine':
            wave = np.sin(self.freq * time_array * 2 * np.pi)
        elif self.wave_type == 'square':
            wave = np.sign(np.sin(self.freq * time_array * 2 * np.pi))
        else:
            wave = np.zeros(num_samples)

        vol_multiplier = max(0, min(self.volume, 100)) / 100.0
        wave = wave * vol_multiplier
        audio_data = np.int16(wave * 32767)
        
        audio_data = np.column_stack((audio_data, audio_data))
        audio_data = np.ascontiguousarray(audio_data)

        sound = pygame.sndarray.make_sound(audio_data)
        sound.play()