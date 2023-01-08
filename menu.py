import pygame

from terminate import terminate
from load_image import load_image
from data import width, height, fps

all_sprites = pygame.sprite.Group()


class Backgraund(pygame.sprite.Sprite):
    im = load_image('backstage', "space-bck1.png")

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Backgraund.im
        self.rect = self.image.get_rect()


class Menu(pygame.sprite.Sprite):
    image = load_image('backstage', 'menu.png')

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Menu.image
        self.x, self.y = width // 2, height // 4
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

    def reverse(self, pos, point):
        if pos[0] in range(self.rect.left, self.rect.right) and \
                pos[1] in range(self.rect.top, self.rect.bottom):
            if point:
                self.image = self.us_image
                return False
            else:
                self.image = self.gu_image
                return True
        return point


sound = False
pygame.mixer.music.load("data/sound/fon.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.pause()


def menu():
    global sound
    running = True

    Backgraund()
    Menu()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 'game', False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if res.checkpress(event.pos):
                    return 'game', False
                if ret.checkpress(event.pos):
                    return 'game', True
                if close.checkpress(event.pos):
                    running = False
                if musc.reverse(event.pos, sound):
                    sound = True
                else:
                    sound = False
        if sound:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()
        res.checkguad(pygame.mouse.get_pos())
        ret.checkguad(pygame.mouse.get_pos())
        close.checkguad(pygame.mouse.get_pos())
        all_sprites.draw(screen)
        all_sprites.update()
        pygame.display.update()
        clock.tick(fps)
    terminate()


clock = pygame.time.Clock()
pygame.init()
screen = pygame.display.set_mode((width, height))

res = Button((load_image('button', 'esume_btn.png'),
              load_image('button', 'esume_btn_pr.png')),
             (width / 2, height // 5 * 2))
ret = Button((load_image('button', 'eturn_btn.png'),
              load_image('button', 'eturn_btn_pr.png')),
             (width / 2, height // 5 * 3))
close = Button((load_image('button', 'exit_btn.png'),
                load_image('button', 'exit_btn_pr.png')),
               (width / 2, height // 5 * 4))
musc = Button((load_image('button', 'musc_off.png'),
               load_image('button', 'musc_on.png')),
              (width - 50, height - 50))
