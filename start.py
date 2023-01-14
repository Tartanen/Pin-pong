import pygame

from data import width, height, fps
from Function import Button, terminate, load_image

is_running = False
all_sprites = pygame.sprite.Group()

menu = {}
for i in range(1, 72):
    menu[i] = load_image('Anime', f'{i}.jpg')
    pygame.transform.scale(menu[i], (width, height))


class Anime(pygame.sprite.Sprite):
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


def start_screen():
    running = True
    Anime()
    start = Button(all_sprites, (load_image('button', 'start_btn.png'),
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
