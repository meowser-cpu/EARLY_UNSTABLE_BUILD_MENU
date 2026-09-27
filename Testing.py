import os
import sys
def manage_output():
    # Check if stdout is an active, interactive terminal (like running in VS Code)
    # Also check if a known debugger is hooked into the script
    is_interactive = sys.stdout and sys.stdout.isatty() or 'debugpy' in sys.modules
    
    if not is_interactive:
        # Hide the Pygame welcome prompt on non-terminal launches
        os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
        
        class DevNull:
            def write(self, msg): pass
            def flush(self): pass

        sys.stdout = DevNull()
        sys.stderr = DevNull()

# Run this before importing pygame
manage_output()
import pygame
import random
from script.Typing import Tone
import math

# NOTE: If you have your songs.py file working, uncomment the line below!
from script.songs import calm_playlist, test_playlist
__import__('os').system('cls' if __import__('os').name == 'nt' else 'clear')



def print_debug_info(message):
    # Check if stdout is an active, interactive terminal (like running in VS Code)
    # Also check if a known debugger is hooked into the script
    is_interactive = sys.stdout and sys.stdout.isatty() or 'debugpy' in sys.modules
    
    if is_interactive:
        print(message)
def feedback(urgency, message,style):
    if 0 == style:
        return{
            "urgency": urgency.upper(),
            "message": message
        }
    elif 1 == style:
        return{
            "error": urgency.upper(),
            "message": message
        }
    elif 2 == style:
        return{
            "log": urgency.upper(),
            "message": message
        }
# ==========================================
# 1. SETUP & VARIABLES
# ==========================================
pygame.init()
print(feedback("info", "manage_output has been executed successfully",2))
screen = pygame.display.set_mode((800, 600))
print(feedback("info", "Display initialized successfully!",2))
pygame.display.set_caption("My Music Visualizer")
print(feedback("info", "Display caption set successfully![My Music Visualizer]",2))

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
Switch = 1
active_freq = 0        
note_end_time = 0      
circle_y = 550   
gravity = 5      
print(feedback("info", "Setup for local variables is complete!",2))
# ==========================================
# 2. THE FUNCTIONS
# ==========================================
#circles are in testing

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

        print_debug_info("--------------------")
        print_debug_info("current time: (" + str(current_time) + ")")
        print_debug_info("--------------------")
        print_debug_info("next note time: (" + str(next_note_time) + ")")
        print_debug_info("--------------------")
        print_debug_info("current note duration: (" + str(dur) + ")")
        print_debug_info("--------------------")
        print_debug_info("current note wait: (" + str(wait) + ")")
        print_debug_info("--------------------")
        print_debug_info("current note frequency: (" + str(freq) + ")")
        print_debug_info("--------------------")
        print_debug_info("current note volume: (" + str(vol) + ")")
        print_debug_info("--------------------")
        print_debug_info("--------------------")
        print_debug_info("current note number: (" + str(current_note) + ")")
        print_debug_info("--------------------")
        if style == 0:
            print_debug_info("synth wave selected: Wait (0)")
            print_debug_info("--------------------")
        elif style == 1:
            print_debug_info("synth wave selected: square (1)")
            print_debug_info("--------------------")
        elif style == 2:
            print_debug_info("synth wave selected: sine (2)")
            print_debug_info("--------------------")
        elif style == 3:
            print_debug_info("synth wave selected: Audio file (3)")
            print_debug_info("--------------------")
        else:
            print_debug_info("--------------------")
            print_debug_info("A ERROR HAS OCCURED WITHIN LINES 74 to 96")
            print_debug_info("it's most likely that you forgot that you forgot to add a zero within the list")
            print_debug_info("check files songs.py and Testing.py")
            print_debug_info("--------------------")
        print_debug_info("0 is wait, 1 is square, 2 is sine, 3 is audio file")
#THIS IS REALLY UNSTABLE please use with caution!
def playlist_choice(play, loop, switch, conforming_switch):
    """Selects a single song allowing: random_song is unfunctional in changeing so this a support function for it."""
    play_random_song(play, loop),
    if current_song == None:
            print_debug_info("Song has ended")
            print_debug_info("now updating")
            if conforming_switch == 1:
                current_song == switch
                play_song(switch, loop),
                print_debug_info("CHECK"+"\n")

# ==========================================
# 3. THE MAIN GAME LOOP
# ==========================================

# A tiny test song just in case you haven't set up songs.py yet!
test_song = [
    (0, 0, 0, 0, 1.0)
]
#known error without a patch currently
#play_song forces test_song to play ONLY
play_song(test_song, loop=False)

#Please note that calm_playlist goes through while test_playlist is ignored
#So basicly what this logic does is if a playlist fails to load you can force a song as a backup.
#So you could have like one playlist as a focus

playlist_choice(calm_playlist,loop=False, switch=test_playlist, conforming_switch=1)




# (If you imported calm_playlist at the top, you can do this instead:)
# plays if test_song going good.


font = pygame.font.Font(None, 64)
trail = []
running = True
while running:
    
    # 1. Update the music sequencer
    update_music()
    

    #  Refresh the screen
    pygame.display.flip()
    
    #  Check for quitting
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
