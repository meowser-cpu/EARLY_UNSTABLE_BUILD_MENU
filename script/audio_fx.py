import pygame
import numpy as np

def make_8bit(sound_object, crush_factor=2048):
    """
    Takes a Pygame Sound object (or a raw NumPy array) and returns a bit-crushed version.
    Automatically handles Stereo/Mono conversions.
    """
    # 1. Pull the raw math array out (or accept an array directly)
    if isinstance(sound_object, pygame.mixer.Sound):
        sound_array = pygame.sndarray.array(sound_object)
    else:
        sound_array = sound_object
    
    # 2. Crush it using the integer division trick
    crushed_array = (sound_array // crush_factor) * crush_factor
    
    # 3. FIX THE DIMENSIONS: Check if mixer is stereo but array is mono
    mixer_settings = pygame.mixer.get_init()
    if mixer_settings:
        channels = mixer_settings[2] 
        
        # If mixer expects 2 channels (stereo) but array is 1D (mono)
        if channels == 2 and len(crushed_array.shape) == 1:
            # Duplicate the mono sound to both the left and right speakers
            crushed_array = np.column_stack((crushed_array, crushed_array))
            
    # 4. Turn it back into a playable Pygame Sound
    return pygame.sndarray.make_sound(crushed_array)