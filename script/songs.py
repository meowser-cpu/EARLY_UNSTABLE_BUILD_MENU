#HOW TO USE THIS
#Style , Volume , Duration , Frequency , Wait Time
#STYLE - there are four types
# 0 is defualt(no sound so it's pretty good for a wait note) - 1 is a square wave - 2 is a sine wave - 3 is a audio file of any choice (:

#VOL - volume is 8000 but that's basicly telling you it on 80% volume for example.
#
#DUR - how long the note you want to last for
#
#FREQ - changes the wave freq and works with audio files to!
#
#Wait time - it delays the next note for a certent amount time.
#
custom_game_loop =[

# Format: (style [1=square, 2=sine], volume, duration(s), frequency(Hz), wait_time(s))
(1, 0.4, 0.15, 220.00, 0.15), # A3
    (1, 0.4, 0.15, 329.63, 0.15), # E4
    (1, 0.4, 0.15, 440.00, 0.15), # A4
    (1, 0.4, 0.15, 523.25, 0.15), # C5
    
    # Melodic Rise (Sine Wave - Smooth transition)
    (2, 0.5, 0.25, 659.25, 0.25), # E5
    (2, 0.5, 0.25, 587.33, 0.25), # D5
    (2, 0.5, 0.25, 523.25, 0.25), # C5
    (2, 0.5, 0.50, 440.00, 0.50), # A4 (Sustain & Pulse)
    
    # Harmonic Accent
    (1, 0.4, 0.10, 349.23, 0.15), # F4
    (1, 0.4, 0.10, 392.00, 0.15), # G4
    (1, 0.4, 0.60, 440.00, 0.60)
]

# FIX: Update your main loop initialization to target the newly generated array
# playlist_choice(custom_game_loop, loop=True, switch=test_playlist, conforming_switch=1)

#test_playlist = [
#    (2, 8000, 0.4, 880, 0.4),
#    (2, 8000, 0.4, 659, 0.4),
#    (1, 4000, 0.4, 440, 0.4)
#]

# 2. Your Playlist!
# It just bundles the songs together so your randomizer can pick one.
calm_playlist = [custom_game_loop]