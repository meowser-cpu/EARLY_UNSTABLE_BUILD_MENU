"""
Module: script/Typing.py
Description: Vectorized procedural audio generation and bitcrush manipulation engine using NumPy and Pygame sndarray.
Governance: A.R.I.A. Framework (Rules 6, 8, 12, 15, 34, 42)
"""

import pygame
import numpy as np
from typing import Optional, Union, List

class Tone:
    """
    Handles real-time mathematical waveform synthesis, sample manipulation, 
    and hardware audio streaming via Pygame's mixer subsystem.
    """

    # Class-level list to prevent Pygame Sound objects from being garbage-collected while playing
    active_sounds: List[pygame.mixer.Sound] = []

    def __init__(
        self, 
        freq: float = 440.0, 
        duration: float = 1.0, 
        wave_type: str = 'crushed', 
        crush_factor: int = 4096
    ) -> None:
        """
        Initializes synthesizer parameters and ensures mixer subsystem readiness.

        Args:
            freq (float): Oscillation frequency in Hertz (Hz).
            duration (float): Playback duration in seconds.
            wave_type (str): Waveform classification ('sine', 'square', 'crushed').
            crush_factor (int): Bitcrush quantization divisor.
        """
        self.freq: float = float(freq)
        self.duration: float = float(duration)
        self.wave_type: str = wave_type
        self.crush_factor: int = crush_factor
        self.sample_rate: int = 44100
        self.volume: float = 0.5  # Standard 0.0 to 1.0 scalar scale
        self.freq_scale: float = 1.0

        # Defensive mixer initialization check
        try:
            if not pygame.get_init():
                pygame.init()
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=self.sample_rate, size=-16, channels=2, buffer=512)
                pygame.mixer.set_num_channels(32)
        except pygame.error as e:
            print(f"[AUDIO ERROR] Mixer initialization failure: {e}")

    def play(self) -> None:
        """
        Generates a mathematically vectorized waveform via NumPy, casts it to 16-bit PCM, 
        maintains a strong reference to prevent garbage collection, and streams it to the mixer.
        """
        if self.duration <= 0.0:
            return

        try:
            # Construct vectorized time domain axis
            total_samples = int(self.sample_rate * self.duration)
            time_axis = np.linspace(0, self.duration, total_samples, endpoint=False)
            
            # Scale scalar volume to 16-bit signed PCM integer peak boundaries
            clamped_volume = max(0.0, min(float(self.volume), 1.0))
            amplitude = clamped_volume * 32767.0 
            
            # Mathematical wave generation
            if self.wave_type == 'square':
                wave = amplitude * np.sign(np.sin(2 * np.pi * self.freq * time_axis))
            elif self.wave_type == 'sine':
                wave = amplitude * np.sin(2 * np.pi * self.freq * time_axis)
            else:  # 'crushed' or fallback default
                wave = amplitude * np.sin(2 * np.pi * self.freq * time_axis)
                if self.crush_factor > 0:
                    wave = (wave // self.crush_factor) * self.crush_factor
                
            # Type casting, stereo interleaving, and memory contiguity for Pygame sndarray
            wave = wave.astype(np.int16)
            stereo_wave = np.column_stack((wave, wave))
            stereo_wave = np.ascontiguousarray(stereo_wave)
            
            sound = pygame.sndarray.make_sound(stereo_wave)
            sound.set_volume(clamped_volume)
            
            # FIX: Prune finished sounds and retain active reference to prevent garbage collection truncation
            Tone.active_sounds = [s for s in Tone.active_sounds if s.get_num_channels() > 0]
            Tone.active_sounds.append(sound)
            
            sound.play()
        except Exception as e:
            print(f"[AUDIO ERROR] Vectorized synthesis failed: {e}")

    def play_file(self, filename: str) -> None:
        """
        Loads an external .wav asset, applies optional bitcrush manipulation, and streams playback.

        Args:
            filename (str): Target path to the audio file.
        """
        try:
            original_sound = pygame.mixer.Sound(filename)
            sound_array = pygame.sndarray.array(original_sound)
            
            if self.wave_type == 'crushed' and self.crush_factor > 0:
                sound_array = (sound_array // self.crush_factor) * self.crush_factor
                
            final_sound = pygame.sndarray.make_sound(sound_array)
            final_sound.set_volume(max(0.0, min(float(self.volume), 1.0)))
            
            # Retain reference for file playback as well
            Tone.active_sounds = [s for s in Tone.active_sounds if s.get_num_channels() > 0]
            Tone.active_sounds.append(final_sound)
            
            final_sound.play()
        except Exception as e:
            print(f"[AUDIO ERROR] Failed to load or play file '{filename}': {e}")