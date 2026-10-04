
import pygame
import numpy as np

# FIX: Ensure this class name matches your main script import (e.g., 'class Tone:' if your main script uses 'my_synth = Tone()')
class Synth:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 512)
        # Note: pygame.init() is already called in the main script, but it is safe here as a redundancy
        pygame.init()
        self.sample_rate = 44100
        self.freq = 440
        self.volume = 0.5 # FIX: Default adjusted to standard 0.0 - 1.0 float scale
        self.duration = 0.5 # FIX: Default adjusted to standard seconds
        self.wave_type = 'sine'
        
    def play(self):
        # FIX: Removed the / 1000.0 division. The main script already passes duration in pure seconds (e.g., 0.15).
        duration_seconds = float(self.duration) 
        
        num_samples = int(duration_seconds * self.sample_rate)
        time_array = np.linspace(0, duration_seconds, num_samples, False)
        
        if self.wave_type == 'sine':
            wave = np.sin(self.freq * time_array * 2 * np.pi)
        elif self.wave_type == 'square':
            wave = np.sign(np.sin(self.freq * time_array * 2 * np.pi))
        else:
            wave = np.zeros(num_samples)

        # FIX: Removed the / 100.0 division. The main array passes volume as a 0.0 to 1.0 multiplier natively.
        vol_multiplier = max(0.0, min(float(self.volume), 1.0))
        wave = wave * vol_multiplier
        
        audio_data = np.int16(wave * 32767)
        
        audio_data = np.column_stack((audio_data, audio_data))
        audio_data = np.ascontiguousarray(audio_data)

        sound = pygame.sndarray.make_sound(audio_data)
        sound.play()