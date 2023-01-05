import pygame

from terminate import terminate
from load_image import load_image

fps = 60
width = 640
height = 1024
is_running = False
all_sprites = pygame.sprite.Group()


class Backgraund(pygame.sprite.Sprite):
    im = load_image("space-bck1.png")

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Backgraund.im
        self.rect = self.image.get_rect()


class Menu(pygame.sprite.Sprite):
    image = load_image('menu.png')

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Menu.image
        self.rect = self.image.get_rect()
        self.rect.center = (width / 2, height // 5)
        self.mask = pygame.mask.from_surface(self.image)


class Button(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        super().__init__(all_sprites)
        self.image = image
        self.x, self.y = pos
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self):
        screen.blit(self.image, self.rect)

    def checkpress(self, pos):
        if pos[0] in range(self.rect.left, self.rect.right) and pos[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False


def start_screen():
    running = True
    Backgraund()
    Menu()

    start = Button(load_image('play.png'), (width / 2, height // 5 * 2))
    option = Button(load_image('options.png'), (width / 2, height // 5 * 3))
    close = Button(load_image('cancel.png'), (width / 2, height // 5 * 4))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start.checkpress(event.pos):
                    return 'game'
                if option.checkpress(event.pos):
                    print('Пoка я (Бодя) не напишу ИИ, оно работать не будет')
                if close.checkpress(event.pos):
                    running = False
        all_sprites.draw(screen)
        all_sprites.update()
        pygame.display.update()
        clock.tick(fps)
    terminate()

clock = pygame.time.Clock()
pygame.init()
screen = pygame.display.set_mode((width, height))


