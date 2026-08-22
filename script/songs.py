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
theme_1 = [
    (1, 8000, 0.2, 440, 0.2),
    (0, 0, 0, 0, 0.5)
]

theme_2 = [
    (2, 8000, 0.4, 880, 0.4),
    (2, 8000, 0.4, 659, 0.4)
]

# 2. Your Playlist!
# It just bundles the songs together so your randomizer can pick one.
calm_playlist = [theme_1, theme_2]