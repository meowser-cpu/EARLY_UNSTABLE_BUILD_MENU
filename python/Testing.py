import pygame
# hall of awesome goobers here(no I won't make the credit boring cause people deserve more than that.)
#line 1 - This tells the code the path that oh hey it using "pygame"

from sys import exit

# line 4 - names pygame.exit() to just exit()

from filesupport_beta import *
#line 8 - calls support from the file filesupport_beta.py it's still in the works.

print("EARLY BUILD 0.0000000000000014") 
#line 12 - How many times I edited this. and you guys too! 
#line 17 to 20 - pygame init allows the setup of screen and clock
#line 17 to 20(screen and clock) - screen is not auto set but set within numbers(like for example your monitor 
#is 1244x1080p and you wanted to set it to 1920x1080p since it's only windows it will kick(to avoid a crash) and say you have an error(I'm not for sure) please don't do it). but for clock it automaticly works and runs a timer.
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

while running:
    
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")
    #defines a circle here. so it can just like
    def area_of_circle(radius):
     pi = 3.14
     area = pi * radius * radius
     return area
    sword_length = 1.0
    spear_length = 2.0
    sword_area = area_of_circle(sword_length)
    spear_area = area_of_circle(spear_length)

    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

exit()