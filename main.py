import pygame
from start_window import start_screen
from load_image import load_image
from game import game
from wins import wins
from menu import menu


def main():
    pygame.display.set_caption('Пин-понг')
    pygame.display.set_icon(load_image('backstage', 'icon.png'))
    scene = ('start', False)
    while True:
        if scene[0] == 'start':
            scene = start_screen()
        elif scene[0] == 'win':
            scene = wins(scene[-1])
        elif scene[0] == 'pause':
            scene = menu()
        elif scene[0] == 'game':
            scene = game(scene[-1])


main()
