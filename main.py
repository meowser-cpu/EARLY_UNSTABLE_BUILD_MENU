import os
import sys
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)
import math
import random

# --- Set working directory to the folder where this script lives ---
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# --- Environment Check ---
vscode = "VSCODE_PID" in os.environ or os.environ.get("TERM_PROGRAM") == "vscode" or "VSCODE_CWD" in os.environ
devmode = True if vscode else False

def manage_output():
    is_interactive = sys.stdout is not None and getattr(sys.stdout, 'isatty', lambda: False)() or 'debugpy' in sys.modules
    
    if not is_interactive:
        os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
        
        class DevNull:
            def write(self, msg): pass
            def flush(self): pass
            def isatty(self): return False

        sys.stdout = DevNull()
        sys.stderr = DevNull()  

manage_output()

import pygame
from script.Typing import Tone
from script.songs import calm_playlist, test_playlist

os.system('cls' if os.name == 'nt' else 'clear')


def print_debug_info(message):
    is_interactive = sys.stdout is not None and getattr(sys.stdout, 'isatty', lambda: False)() or 'debugpy' in sys.modules
    if is_interactive:
        print(message)


def feedback(urgency, message, style):
    global devmode
    if not devmode:
        return ""
    
    styles = {
        0: {"urgency": urgency.upper(), "message": message},
        1: {"error": urgency.upper(), "message": message},
        2: {"log": urgency.upper(), "message": message}
    }
    return styles.get(style, message)

# ==========================================
# 1. SETUP & VARIABLES
# ==========================================
pygame.init()
print(feedback("info", "manage_output has been executed successfully", 2))

# Initial screen setup with RESIZABLE flag enabled
screen_w, screen_h = 800, 600
screen = pygame.display.set_mode((screen_w, screen_h), pygame.RESIZABLE)
print(feedback("info", "Display initialized with RESIZABLE support!", 2))

pygame.display.set_caption("My Music Visualizer")
print(feedback("info", "Display caption set successfully![My Music Visualizer]", 2))

my_synth = Tone()

# Trackers
current_song = None
current_note = 0
next_note_time = 0
loop_current_song = True 
Switch = 1
active_freq = 0        
note_end_time = 0      
gravity = 5      
print(feedback("info", "Setup for local variables is complete!", 2))

# --- Dynamic Grayscale Color Interpolation Engine ---
grayscale_active = False  
grayscale_factor = 0.0    

def get_grayscale_color(color, factor):
    """Linearly interpolates an RGB color toward luminance grayscale based on factor."""
    r, g, b = color[:3]  
    gray = int(0.299 * r + 0.587 * g + 0.114 * b)  
    r_out = int(r + (gray - r) * factor)  
    g_out = int(g + (gray - g) * factor)  
    b_out = int(b + (gray - b) * factor)  
    return (r_out, g_out, b_out)  

# --- Floating Button Initialization ---
button_rel_pos = (0.875, 0.208)  # Scaled relative position (~700/800, ~125/600)
button_center = (int(screen_w * button_rel_pos[0]), int(screen_h * button_rel_pos[1]))
btn_x, btn_y = float(button_center[0]), float(button_center[1])
button_base_size = 60      
button_zoomed = False
button_scale = 1.0

try:
    button_img = pygame.image.load("floating.png")  
    base_button_surface = pygame.transform.scale(button_img, (button_base_size, button_base_size))  
except (pygame.error, FileNotFoundError):
    base_button_surface = pygame.Surface((button_base_size, button_base_size), pygame.SRCALPHA)  
    pygame.draw.circle(base_button_surface, (0, 255, 200, 220), (30, 30), 28)  
    pygame.draw.circle(base_button_surface, (255, 255, 255, 240), (30, 30), 14)     

button_rect = base_button_surface.get_rect(center=button_center)  

# --- Full-Screen Background Image Initialization ---
img_x, img_y = screen_w / 2.0, screen_h / 2.0  
bg_zoomed = False      
bg_scale = 1.0         

try:
    float_img = pygame.image.load("floating.png")  
except (pygame.error, FileNotFoundError):
    float_img = pygame.Surface((880, 660), pygame.SRCALPHA)  
    float_img.fill((18, 22, 42, 180))  
    pygame.draw.circle(float_img, (0, 210, 255, 40), (440, 330), 280)  
    pygame.draw.circle(float_img, (160, 60, 255, 30), (440, 330), 180)  

def update_background_surface(w, h):
    """Rescales background image base dimensions relative to screen size."""
    bg_w, bg_h = int(w * 1.1), int(h * 1.1)
    return pygame.transform.scale(float_img, (bg_w, bg_h)), bg_w, bg_h

float_surface, bg_w, bg_h = update_background_surface(screen_w, screen_h)

# ==========================================
# 2. FUNCTIONS
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
    if playlist:
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
            
            active_freq = freq
            note_end_time = current_time + int(dur * 1000)
            
            if style == 1:
                my_synth.wave_type = 'square'
            elif style == 2:
                my_synth.wave_type = 'sine'
                
            my_synth.play()
            
        next_note_time = current_time + int(wait * 1000)
        current_note += 1

def playlist_choice(play, loop, switch, conforming_switch):
    """Selects a song from 'play' or falls back to 'switch' if empty."""
    global current_song
    
    play_random_song(play, loop)
    
    if current_song is None:
        if conforming_switch == 1:
            current_song = switch
            play_song(switch, loop)

# ==========================================
# 3. MAIN GAME LOOP
# ==========================================
test_song = [(0, 0, 0, 0, 1.0)]
play_song(test_song, loop=False)

playlist_choice(calm_playlist, loop=False, switch=test_playlist, conforming_switch=1)

font = pygame.font.Font(None, 64)
running = True
clock = pygame.time.Clock()

base_bg_color = (12, 14, 28)  

while running:
    update_music()
    
    # Get current dynamic window dimensions
    screen_w, screen_h = screen.get_size()
    center_x, center_y = screen_w // 2, screen_h // 2
    button_center = (int(screen_w * button_rel_pos[0]), int(screen_h * button_rel_pos[1]))

    # Dynamic Left Margin Gradient Fade Width
    fade_width = max(100, int(screen_w * 0.31))

    # Smooth Grayscale Transition Factor Update
    target_factor = 1.0 if grayscale_active else 0.0  
    if grayscale_factor < target_factor:  
        grayscale_factor = min(1.0, grayscale_factor + 0.04)  
    elif grayscale_factor > target_factor:  
        grayscale_factor = max(0.0, grayscale_factor - 0.04)  
        
    current_bg = get_grayscale_color(base_bg_color, grayscale_factor)  
    screen.fill(current_bg)  
    
    current_time = pygame.time.get_ticks()

    # --- Background Parallax Motion & Scaling ---
    target_bg_scale = 1.40 if bg_zoomed else 1.00
    bg_scale += (target_bg_scale - bg_scale) * 0.08  

    mouse_x, mouse_y = pygame.mouse.get_pos()  
    
    target_img_x = center_x - (mouse_x - center_x) * 0.05  
    target_img_y = center_y - (mouse_y - center_y) * 0.05  
    
    img_x += (target_img_x - img_x) * 0.08  
    img_y += (target_img_y - img_y) * 0.08  
    
    # Render full-screen background image (LAYER 1 - Behind Waves)
    cur_w = max(1, int(bg_w * bg_scale))
    cur_h = max(1, int(bg_h * bg_scale))
    scaled_bg = pygame.transform.smoothscale(float_surface, (cur_w, cur_h))
    
    float_render_surface = scaled_bg.copy()  
    if grayscale_factor > 0.0:  
        dark_alpha = int(120 * grayscale_factor)  
        tint_overlay = pygame.Surface(float_render_surface.get_size(), pygame.SRCALPHA)  
        tint_overlay.fill((100, 100, 100, dark_alpha))  
        float_render_surface.blit(tint_overlay, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)  
        
    float_rect = float_render_surface.get_rect(center=(int(img_x), int(img_y)))  
    screen.blit(float_render_surface, float_rect)  
    
    # --- Sine Wave Rendering Engine (LAYER 2 - Centered vertically relative to screen_h) ---
    is_note_active = current_time < note_end_time
    base_amp = 35.0 if is_note_active else 12.0
    freq_boost = (active_freq / 25.0) if is_note_active else 0.0
    total_amp = min(110.0, base_amp + freq_boost)
    
    wave_midline = center_y
    base_wave_layers = [
        {"color": (0, 210, 255), "speed": 0.004, "freq_scale": 0.015, "offset_y": wave_midline, "amp_mult": 1.0},
        {"color": (160, 60, 255), "speed": 0.003, "freq_scale": 0.010, "offset_y": wave_midline, "amp_mult": 0.75},
        {"color": (255, 30, 140), "speed": 0.006, "freq_scale": 0.022, "offset_y": wave_midline, "amp_mult": 0.45}
    ]
    
    for layer in base_wave_layers:
        points = []
        phase = current_time * layer["speed"]
        wave_color = get_grayscale_color(layer["color"], grayscale_factor)  
        for x in range(0, screen_w + 5, 5):
            y = layer["offset_y"] + math.sin(x * layer["freq_scale"] + phase) * (total_amp * layer["amp_mult"])
            points.append((x, int(y)))
        if len(points) > 1:
            pygame.draw.lines(screen, wave_color, False, points, 3)  
            
    # --- Dynamic Left Margin Gradient Fade (LAYER 3 - Dynamic Height & Width) ---
    fade_surface = pygame.Surface((fade_width, screen_h), pygame.SRCALPHA)  
    for x in range(fade_width):  
        alpha = int(255 * (1.0 - (x / fade_width)))  
        pygame.draw.line(fade_surface, (current_bg[0], current_bg[1], current_bg[2], alpha), (x, 0), (x, screen_h))  
    screen.blit(fade_surface, (0, 0))  

    # --- Interactive Floating Button (LAYER 4 - Dynamically Positioned Above Waves) ---
    target_btn_x = button_center[0] - (mouse_x - center_x) * 0.008
    target_btn_y = button_center[1] - (mouse_y - center_y) * 0.008
    btn_x += (target_btn_x - btn_x) * 0.08
    btn_y += (target_btn_y - btn_y) * 0.08

    target_btn_scale = 1.30 if button_zoomed else 1.00
    button_scale += (target_btn_scale - button_scale) * 0.15
    btn_size = max(1, int(button_base_size * button_scale))

    scaled_btn_surface = pygame.transform.smoothscale(base_button_surface, (btn_size, btn_size))
    btn_render_surface = scaled_btn_surface.copy()

    if grayscale_factor > 0.0:
        dark_alpha = int(120 * grayscale_factor)
        tint_overlay = pygame.Surface(btn_render_surface.get_size(), pygame.SRCALPHA)
        tint_overlay.fill((100, 100, 100, dark_alpha))
        btn_render_surface.blit(tint_overlay, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    button_rect = btn_render_surface.get_rect(center=(int(btn_x), int(btn_y)))
    screen.blit(btn_render_surface, button_rect)  

    pygame.display.flip()
    clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            # Handle dynamic surface scaling when resizing the window
            screen_w, screen_h = event.w, event.h
            screen = pygame.display.set_mode((screen_w, screen_h), pygame.RESIZABLE)
            float_surface, bg_w, bg_h = update_background_surface(screen_w, screen_h)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  
            if button_rect.collidepoint(event.pos):  
                grayscale_active = not grayscale_active  
                bg_zoomed = not bg_zoomed  
                button_zoomed = not button_zoomed
                print_debug_info(f"Grayscale: {grayscale_active} | Background Zoomed: {bg_zoomed}")  

pygame.quit()