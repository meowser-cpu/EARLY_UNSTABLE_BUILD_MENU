import pygame
from os.path import join
def import_image(*path, alpha = True, format = 'jpg'):
    full_path = join(*path) + f'.{format}'
    surf = pygame.image.load(full_path).convert_alpha() if alpha else pygame.image.load(full_path).convert()
    return surf