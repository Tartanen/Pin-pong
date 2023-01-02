import pygame
import sys

from load_image import load_image


fps = 60
width = 640
height = 1024

screen = pygame.display.set_mode((width, height))

width = screen.get_width()
height = screen.get_height()

all_sprites = pygame.sprite.Group()
menu_sprites = pygame.sprite.Group()
back_sprites = pygame.sprite.Group()
class Menu(pygame.sprite.Sprite):
    image = load_image('menu.png')

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Menu.image
        self.rect = self.image.get_rect()
        self.rect.center = (width / 2, height // 5)
        self.mask = pygame.mask.from_surface(self.image)


class Start(pygame.sprite.Sprite):
    image = load_image('play.png')

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Start.image
        self.rect = self.image.get_rect()
        self.rect.center = (width / 2, height // 5 * 2)
        self.mask = pygame.mask.from_surface(self.image)


class Option(pygame.sprite.Sprite):
    image = load_image('options.png')

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Option.image
        self.rect = self.image.get_rect()
        self.rect.center = (width / 2, height // 5 * 3)
        self.mask = pygame.mask.from_surface(self.image)


class Close(pygame.sprite.Sprite):
    image = load_image('cancel.png')

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Close.image
        self.rect = self.image.get_rect()
        self.rect.center = (width / 2, height // 5 * 4)
        self.mask = pygame.mask.from_surface(self.image)



class Backgraund(pygame.sprite.Sprite):
    im = load_image("space-bck1.png")

    def __init__(self):
        super().__init__(back_sprites)
        self.image = Backgraund.im
        self.rect = self.image.get_rect()


def click(obj, x, y):
    pass


pygame.init()

smallfont = pygame.font.SysFont('Corbel', 35)
running = True

Backgraund()
Menu()
Start()
Option()
Close()

while running:

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False

    back_sprites.draw(screen)
    back_sprites.update()
    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.flip()
pygame.quit()
