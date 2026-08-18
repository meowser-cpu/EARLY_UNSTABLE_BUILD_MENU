import pygame
import random
from Typing import Tone

# NOTE: If you have your songs.py file working, uncomment the line below!
from songs import calm_playlist 

# ==========================================
# 1. SETUP & VARIABLES
# ==========================================
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("My Music Visualizer")

my_synth = Tone()

# --- Background Image Setup ---
#try:
#    # Change this to your exact image file name!
#    background_image = pygame.image.load("your_image_here.png").convert()
#    background_image = pygame.transform.scale(background_image, (800, 600))
#except pygame.error:
#    print("Warning: Could not find background image. Falling back to black.")
#    background_image = None

# --- Music & Visualizer Trackers ---
current_song = None
current_note = 0
next_note_time = 0
loop_current_song = True 

active_freq = 0        
note_end_time = 0      
circle_y = 550   
gravity = 5      


# ==========================================
# 2. THE FUNCTIONS
# ==========================================


def play_song(song_list, loop=True):
    """Loads a new song and resets the trackers."""
    global current_song, current_note, next_note_time, loop_current_song
    current_song = song_list
    current_note = 0  
    loop_current_song = loop  
    next_note_time = pygame.time.get_ticks()

def play_random_song(playlist, loop=True):
    """Picks a random song from a playlist and plays it."""
    chosen_song = random.choice(playlist)
    play_song(chosen_song, loop)

def update_music():
    """Reads the song list and plays the notes in the background."""
    global current_song, current_note, next_note_time, loop_current_song
    global active_freq, note_end_time 
    
    if current_song is None:
        return
        
    if current_note >= len(current_song):
        if loop_current_song:
            current_note = 0
        else:
            current_song = None
            return
            
    current_time = pygame.time.get_ticks()
    
    if current_time >= next_note_time:
        style, vol, dur, freq, wait = current_song[current_note]
        
        if style != 0:
            my_synth.volume = vol
            my_synth.duration = dur
            my_synth.freq = freq
            
            # Update visuals!
            active_freq = freq
            note_end_time = current_time + int(dur * 1000)
            
            if style == 1:
                my_synth.wave_type = 'square'
            elif style == 2:
                my_synth.wave_type = 'sine'
                
            my_synth.play()
            
        next_note_time = current_time + int(wait * 1000)
        current_note += 1


# ==========================================
# 3. THE MAIN GAME LOOP
# ==========================================

# A tiny test song just in case you haven't set up songs.py yet!
test_song = [
    (1, 8000, 0.2, 440, 0.5), 
    (2, 8000, 0.5, 880, 0.5), 
    (0, 0, 0, 0, 1.0)
]
play_song(test_song, loop=True)

# (If you imported calm_playlist at the top, you can do this instead:)
# play_random_song(calm_playlist, loop=True)


running = True
while running:
    
    # 1. Update the music sequencer
    update_music()
    


    # 6. Refresh the screen
    pygame.display.flip()
    
    # 7. Check for quitting
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()