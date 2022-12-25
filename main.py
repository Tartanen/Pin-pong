import os
import random
import sys

import pygame

from data import max_speed_ball, min_speed_ball

fps = 60
width = 640
height = 1024

screen = pygame.display.set_mode((width, height))

horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Rocket1(pygame.sprite.Sprite):
    image = load_image('rocket1.png')

    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites)
        self.image = Rocket1.image
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.mask = pygame.mask.from_surface(self.image)
        self.pos = pos_x, pos_y


class Rocket2(pygame.sprite.Sprite):
    image = load_image('rocket2.png')

    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites)
        self.image = Rocket2.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.pos = pos_x, pos_y


class Ball(pygame.sprite.Sprite):
    image = load_image("ball.png")

    def __init__(self, pos):
        super().__init__(all_sprites)
        self.image = Ball.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        temp = [1, -1, 0]
        self.vx = random.randint(min_speed_ball, max_speed_ball) * random.choice(temp)
        self.vy = random.randint(min_speed_ball, max_speed_ball) * random.choice(temp[0:1])
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            hit.play()
            self.vy = -self.vy
        if pygame.sprite.spritecollideany(self, vertical_borders):
            hit.play()
            self.vx = -self.vx


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)


class Backgraund(pygame.sprite.Sprite):
    image = load_image("space-bck.png")

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Backgraund.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.bottom = height


def move(obj, rule):
    x, y = obj.pos
    if rule == 'left_d' and x > 0:
        obj.move(x + 1, y)
    if rule == 'left_a' and x < width:
        obj.move(x - 1, y)
    if rule == 'left_s' and x > 0:
        obj.move(x - 1, y)
    if rule == 'right_s' and x < width:
        obj.move(x + 1, y)


clock = pygame.time.Clock()
pygame.display.set_caption('Пин-понг')

icon = load_image('icon.png')
pygame.display.set_icon(icon)

pygame.init()

Border(5, 5, 5, height - 5)
Border(width - 5, 5, width - 5, height - 5)

pygame.mixer.music.load("sound/fon.mp3")
hit = pygame.mixer.Sound("sound/hit.mp3")

player1 = Rocket1(height // 2, 20)
player2 = Rocket2(height // 2, width - 20)

backgraund = Backgraund()

clock = pygame.time.Clock()
running = True

pygame.mixer.music.play(-1)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            Ball(event.pos)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move(player1, 'left')
            if event.key == pygame.K_RIGHT:
                move(player1, 'right')
            if event.key == pygame.K_a:
                move(player2, 'left')
            if event.key == pygame.K_d:
                move(player2, 'right')
    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.flip()
    clock.tick(fps)
pygame.quit()
