import random

import pygame

from data import max_speed_ball, min_speed_ball, speed_player1, speed_player2
from load_image import load_image
from load_sound import load_sound

fps = 60
width = 640
height = 1024

screen = pygame.display.set_mode((width, height))

horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
back_sprites = pygame.sprite.Group()

clock = pygame.time.Clock()
pygame.display.set_caption('Пин-понг')

icon = load_image('icon.png')
pygame.display.set_icon(icon)

start = False


def move(obj, rule, rep):
    x, y = obj.pos
    if rule == 'right_d' and x + obj.image.get_rect().size[0] < width - 5:
        for i in range(rep):
            obj.move(x + speed_player2, y)
    if rule == 'left_a' and x > 5:
        for i in range(rep):
            obj.move(x - speed_player2, y)
    if rule == 'left_s' and x > 5:
        for i in range(rep):
            obj.move(x - speed_player1, y)
    if rule == 'right_s' and x + obj.image.get_rect().size[0] < width - 5:
        for i in range(rep):
            obj.move(x + speed_player1, y)
    if rule == 'up' and y - obj.image.get_rect().size[1] < 30:
        for i in range(rep):
            obj.move(x, y - speed_player1)
    if rule == 'down' and y + obj.image.get_rect().size[1] < width - 20:
        for i in range(rep):
            obj.move(x, y + speed_player1)


class Rocket1(pygame.sprite.Sprite):
    image = load_image('rocket11.png')

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Rocket1.image
        pos_x = width / 2 - self.image.get_rect().size[0] / 2
        pos_y = height - self.image.get_rect().size[-1] - 20
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.pos = pos_x, pos_y

    def move(self, x, y):
        self.pos = x, y
        self.rect = self.image.get_rect().move(x, y)


class Rocket2(pygame.sprite.Sprite):
    image = load_image('rocket22.png')

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Rocket2.image
        pos_x = width / 2 - self.image.get_rect().size[0] / 2
        pos_y = 5
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.pos = pos_x, pos_y

    def move(self, x, y):
        self.pos = x, y
        self.rect = self.image.get_rect().move(x, y)


class Ball(pygame.sprite.Sprite):
    def __init__(self, radius, x, y):
        super().__init__(all_sprites)
        self.radius = radius
        self.image = pygame.Surface((2 * radius, 2 * radius),
                                    pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("red"),
                           (radius, radius), radius)
        self.rect = pygame.Rect(x, y, 2 * radius, 2 * radius)
        self.vx = random.randint(-5, 5)
        self.vy = random.randrange(-5, 5)

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.vy = -self.vy
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.vx = -self.vx

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.collide_mask(self, player1):
            hit.play()
            temp = [2, 1, -1, -2]
            mn = random.choice(temp)
            self.vy = -self.vy + mn
            self.vx -= mn
        if pygame.sprite.collide_mask(self, player2):
            hit.play()
            temp = [2, 1, -1, -2]
            mn = random.choice(temp)
            self.vy = -self.vy + mn
            self.vx -= mn
        if pygame.sprite.spritecollideany(self, vertical_borders):
            hit.play()
            self.vx = -self.vx
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            loss.play()


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class Backgraund(pygame.sprite.Sprite):
    im = load_image("space-bck1.png")

    def __init__(self):
        super().__init__(back_sprites)
        self.image = Backgraund.im
        self.rect = self.image.get_rect()


pygame.init()

m_left_s = False
m_right_s = False
m_left_a = False
m_right_d = False

Border(5, 5, width - 5, 5)
Border(5, height - 5, width - 5, height - 5)
Border(5, 5, 5, height - 5)
Border(width - 5, 5, width - 5, height - 5)

pygame.mixer.music.load("data/sound/fon.mp3")
hit = load_sound("hit.mp3")
loss = load_sound("loss.mp3")

clock = pygame.time.Clock()

pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.3)

running = True

Backgraund()
player1 = Rocket1()
player2 = Rocket2()

move(player1, 'left_s', 1)
move(player2, 'left_s', 1)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                m_left_s = True
            if event.key == pygame.K_RIGHT:
                m_right_s = True
            if event.key == pygame.K_a:
                m_left_a = True
            if event.key == pygame.K_d:
                m_right_d = True
            if event.key == pygame.K_g:
                Ball(width // 2, height // 2)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                m_left_s = False
            if event.key == pygame.K_RIGHT:
                m_right_s = False
            if event.key == pygame.K_a:
                m_left_a = False
            if event.key == pygame.K_d:
                m_right_d = False
    if m_left_s:
        move(player1, 'left_s', 1)
    if m_right_s:
        move(player1, 'right_s', 1)
    if m_left_a:
        move(player2, 'left_a', 1)
    if m_right_d:
        move(player2, 'right_d', 1)

    back_sprites.draw(screen)
    back_sprites.update()
    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.flip()
    clock.tick(fps)
pygame.quit()
