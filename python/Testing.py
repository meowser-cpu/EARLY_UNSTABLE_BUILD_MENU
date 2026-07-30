import pygame
# hall of awesome goobers here(no I won't make the credit boring cause people deserve more than that.)
#line 1 - This tells the code the path that oh hey it using "pygame"

from sys import exit

# line 4 - names pygame.exit() to just exit()

from filesupport_beta import *
#line 8 - calls support from the file filesupport_beta.py it's still in the works.

print("EARLY BUILD 0.0000000000000015") 
#line 12 - How many times I edited this. and you guys too! 
#line 17 to 20 - pygame init allows the setup of screen and clock
#line 17 to 20(screen and clock) - screen is not auto set but set within numbers(like for example your monitor 
#is 1244x1080p and you wanted to set it to 1920x1080p since it's only windows it will kick(to avoid a crash) and say you have an error(I'm not for sure) please don't do it). but for clock it automaticly works and runs a timer.
pygame.init()
screen = pygame.display.set_mode((1280, 720))
surf = import_image('graphics', 'candle')
clock = pygame.time.Clock()

while True:
    
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.QUIT
            exit()
    # RENDER YOUR GAME HERE


    screen.fill('black')
    screen.blit(surf,(0,0))
    pygame.display.update()

    clock.tick(60)  # limits FPS to 60