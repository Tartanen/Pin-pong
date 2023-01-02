import sys
import os
import pygame

def load_sound(name):
    fullname = os.path.join('data\sound', name)
    if not os.path.isfile(fullname):
        print(f"Файл с аудио '{fullname}' не найден")
        sys.exit()
    sound = pygame.mixer.Sound(fullname)
    return sound