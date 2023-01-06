import pygame
from menu import start_screen
from load_image import load_image
from game import game
from wins import wins


fps = 60
width = 640
height = 1024


def main():
    pygame.display.set_caption('Пин-понг')
    pygame.display.set_icon(load_image('icon.png'))
    screen = pygame.display.set_mode((width, height))
    scene = 'menu'
    while True:
        if scene == 'menu':
            scene = start_screen()
        elif scene == 'cont':
            scene = wins()
        elif scene == 'game':
            scene = game()

main()

