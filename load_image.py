import sys
import os
import pygame


def load_image(name1, name2, colorkey=None):
    '''
    Да, самый первобытный, но по факту почему-то альфа не работат
    (из-за изображений)
    '''
    fullname = os.path.join('data', 'image', name1, name2)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image
