import pygame

from Function import Button, Backgraund, terminate, load_image
from data import width, height, fps

all_sprites = pygame.sprite.Group()


class Backstage(pygame.sprite.Sprite):
    image = load_image('backstage', 'backstage.png')

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Backstage.image
        self.x, self.y = width // 2, height // 4
        self.rect = self.image.get_rect(center=(self.x, self.y))


class Winners(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__(all_sprites)
        self.image = image
        self.x, self.y = width // 2, height // 2
        self.rect = self.image.get_rect(center=(self.x, self.y))


def wins(player):
    Backgraund(all_sprites, load_image('backstage', "space-bck1.png"))
    Backstage()
    if player:
        Winners(load_image('backstage', 'blue_pl.png'))
    else:
        Winners(load_image('backstage', 'red_pl.png'))
    running = True
    back = Button(all_sprites, (load_image('button', 'back_btn.png'),
                                load_image('button', 'back_btn_pr.png')),
                  (40, 40))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 'start', False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back.checkpress(event.pos):
                    return 'start', False
        back.checkguad(pygame.mouse.get_pos())
        all_sprites.draw(screen)
        all_sprites.update()
        pygame.display.update()
        clock.tick(fps)
    terminate()


clock = pygame.time.Clock()
pygame.init()
screen = pygame.display.set_mode((width, height))
