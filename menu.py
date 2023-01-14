import pygame

from data import width, height, fps
from Function import Button, Backgraund, load_image, terminate

all_sprites = pygame.sprite.Group()


class Menu(pygame.sprite.Sprite):
    image = load_image('backstage', 'menu.png')

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Menu.image
        self.x, self.y = width // 2, height // 4
        self.rect = self.image.get_rect(center=(self.x, self.y))


sound = False
pygame.mixer.music.load("data/sound/fon.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.pause()


def menu():
    global sound
    running = True

    Backgraund(all_sprites, load_image('backstage', "space-bck1.png"))
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

res = Button(all_sprites, (load_image('button', 'esume_btn.png'),
                           load_image('button', 'esume_btn_pr.png')),
             (width / 2, height // 5 * 2))
ret = Button(all_sprites, (load_image('button', 'eturn_btn.png'),
                           load_image('button', 'eturn_btn_pr.png')),
             (width / 2, height // 5 * 3))
close = Button(all_sprites, (load_image('button', 'exit_btn.png'),
                             load_image('button', 'exit_btn_pr.png')),
               (width / 2, height // 5 * 4))
musc = Button(all_sprites, (load_image('button', 'musc_off.png'),
                            load_image('button', 'musc_on.png')),
              (width - 50, height - 50))
