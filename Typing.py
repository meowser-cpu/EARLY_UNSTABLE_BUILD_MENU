#https://www.youtube.com/watch?v=egW_J4et4HA I still don't have a soild understanding of it due to lack of socal posts about audio
import pygame
import numpy as np

class Tone:
    def __init__(self, freq=440, duration=1.0, wave_type='crushed', crush_factor=4096):
        self.freq = freq
        self.duration = duration
        self.wave_type = wave_type
        self.crush_factor = crush_factor
        self.sample_rate = 44100
        self.volume = 10000
        
        if not pygame.mixer.get_init():
            pygame.mixer.init(frequency=self.sample_rate, size=-16, channels=2)

    def play(self):
        """Generates a wave from scratch and plays it."""
        time = np.linspace(0, self.duration, int(self.sample_rate * self.duration), False)
        
        if self.wave_type == 'square':
            wave = self.volume * np.sign(np.sin(2 * np.pi * self.freq * time))
        else:
            wave = self.volume * np.sin(2 * np.pi * self.freq * time)
            
        if self.wave_type == 'crushed':
            wave = (wave // self.crush_factor) * self.crush_factor
            
        wave = wave.astype(np.int16)
        stereo_wave = np.column_stack((wave, wave))
        stereo_wave = np.ascontiguousarray(stereo_wave)
        
        sound = pygame.sndarray.make_sound(stereo_wave)
        sound.play()

    def play_file(self, filename):
        """Loads an audio file, applies effects, and plays it."""
        # 1. Load the original file
        original_sound = pygame.mixer.Sound(filename)
        
        # 2. Extract the raw math array from the file
        sound_array = pygame.sndarray.array(original_sound)
        
        # 3. Apply the crush effect if requested
        if self.wave_type == 'crushed':
            sound_array = (sound_array // self.crush_factor) * self.crush_factor
            
        # 4. Turn it back into a playable sound
        final_sound = pygame.sndarray.make_sound(sound_array)
        
        # 5. Set the volume! 
        # Pygame's built-in set_volume uses a scale from 0.0 to 1.0. 
        # We divide your custom volume (0-32767) by 32767 to make it match!
        calculated_volume = self.volume / 32767.0
        final_sound.set_volume(calculated_volume)
        
        # 6. Play it
        final_sound.play()