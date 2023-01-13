import pygame

from Function import terminate
from load_image import load_image
from data import width, height, fps

all_sprites = pygame.sprite.Group()


class Backgraund(pygame.sprite.Sprite):
    im = load_image('backstage', "space-bck1.png")

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Backgraund.im
        self.rect = self.image.get_rect()


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


class Button(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        super().__init__(all_sprites)
        self.us_image = image[0]
        self.gu_image = image[1]
        self.image = self.us_image
        self.x, self.y = pos
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self):
        screen.blit(self.image, self.rect)

    def checkpress(self, pos):
        if pos[0] in range(self.rect.left, self.rect.right) and \
                pos[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def checkguad(self, pos):
        if pos[0] in range(self.rect.left, self.rect.right) and \
                pos[1] in range(self.rect.top, self.rect.bottom):
            self.image = self.gu_image
        else:
            self.image = self.us_image


def wins(player):
    Backgraund()
    Backstage()
    if player:
        Winners(load_image('backstage', 'blue_pl.png'))
    else:
        Winners(load_image('backstage', 'red_pl.png'))
    running = True
    back = Button((load_image('button', 'back_btn.png'),
                   load_image('button', 'back_btn_pr.png')), (40, 40))
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
