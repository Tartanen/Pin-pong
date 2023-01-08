import pygame

from load_image import load_image
from terminate import terminate
from data import width, height, fps

is_running = False
all_sprites = pygame.sprite.Group()

menu = {}
for i in range(1, 72):
    menu[i] = load_image('Anime', f'{i}.jpg')
    pygame.transform.scale(menu[i], (width, height))


class Backgraund(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.frame = 1
        self.image = menu[self.frame]
        self.rect = self.image.get_rect()

    def update(self):
        self.frame = self.frame % 71
        self.frame += 1
        self.image = menu[self.frame]
        screen.blit(self.image, self.rect)


class Menu(pygame.sprite.Sprite):
    image = load_image('backstage', 'welcome.png')

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Menu.image
        self.x, self.y = width // 2, height // 4
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self):
        screen.blit(self.image, self.rect)


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
        if pos[0] in range(self.rect.left, self.rect.right) and pos[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def checkguad(self, pos):
        if pos[0] in range(self.rect.left, self.rect.right) and pos[1] in range(self.rect.top, self.rect.bottom):
            self.image = self.gu_image
        else:
            self.image = self.us_image


def start_screen():
    running = True
    Backgraund()
    start = Button((load_image('button', 'start_btn.png'),
                    load_image('button', 'start_btn_pr.png')),
                   (width / 2, height // 2))
    Menu()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start.checkpress(event.pos):
                    return 'game', True
        start.checkguad(pygame.mouse.get_pos())
        all_sprites.draw(screen)
        all_sprites.update()
        menu.update()
        pygame.display.update()
        clock.tick(fps // 3)
    terminate()


clock = pygame.time.Clock()
pygame.init()
screen = pygame.display.set_mode((width, height))
