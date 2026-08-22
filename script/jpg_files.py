import pygame
from os.path import join
from os import walk
# line 3 - imports the join function which allows code to open folder more easily.
def import_image(*path, alpha = True, format = 'jpg'):
    #line 4 - def import_image *path finds the path of any listed alpha list if it needs to be alpha or not format is just file type ex .png .gif
    full_path = join(*path) + f'.{format}'
    #line 6 - full_path opens a folder 
    surf = pygame.image.load(full_path).convert_alpha() if alpha else pygame.image.load(full_path).convert()
    #line 8 - surf allows it so you can easily list what images you want loaded or not!(also still letting flexablity)
    return surf
def import_folder(*path):
    frames = []
    for folder_path, sub_folders, image_names in walk(join(*path)):
        for image_name in sorted(image_name, key = lambda name: int(name.split('.')[0])): 
            full_path = join(folder_path, image_name)
            surf = pygame.image.load(full_path).convert_alpha()
            frames.append(surf)
    return frames