import pygame
from script.Typing import Tone
my_synth = Tone()
print("If you don't hear any of the beeps It may be due to corruption")
# Now you can use it, edit it, and call it anywhere in this file!
loop = None
class SoundManager:
    def __init__(self, synth):
        self.my_synth = synth
        self.last_note_time = 0

    def note(self, style, vol, dur, freq):
        self.my_synth.freq = freq * 100
        self.my_synth.volume = vol
        self.my_synth.duration = dur
        
        wave_types = {0: 'crushed', 1: 'square', 2: 'sine'}
        if style in wave_types:
            self.my_synth.wave_type = wave_types[style]
            self.my_synth.play()

    def play_if_ready(self, current_time, wait_time, style, vol, dur, freq):
        if current_time - self.last_note_time >= wait_time:
            self.note(style, vol, dur, freq)
            self.last_note_time = current_time
            return True
        return False