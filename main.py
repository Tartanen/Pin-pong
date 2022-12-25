import random

import pygame

from data import max_speed_ball, min_speed_ball, speed_player1, speed_player2, max_speed_player1, max_speed_player2
from load_image import load_image

fps = 60
width = 640
height = 1024

screen = pygame.display.set_mode((width, height))

horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

clock = pygame.time.Clock()
pygame.display.set_caption('Пин-понг')

icon = load_image('icon.png')
pygame.display.set_icon(icon)


class Rocket1(pygame.sprite.Sprite):
    image = load_image('rocket1.png')

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Rocket1.image
        pos_x = width / 2 - (self.image.get_rect().size)[0] / 2
        pos_y = height - (self.image.get_rect().size)[-1] * 2
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.pos = pos_x, pos_y

    def move(self, x, y):
        self.pos = x, y
        self.rect = self.image.get_rect().move(speed_player1 + x, y)


class Rocket2(pygame.sprite.Sprite):
    image = load_image('rocket2.png')

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Rocket2.image
        pos_x = width / 2 - (self.image.get_rect().size)[0] / 2
        pos_y = (self.image.get_rect().size)[-1] / 2
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.pos = pos_x, pos_y

    def move(self, x, y):
        self.pos = x, y
        self.rect = self.image.get_rect().move(speed_player2 + x + 15, y)


class Ball(pygame.sprite.Sprite):
    image = load_image("ball.png")

    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites)
        self.image = Ball.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        temp = [1, -1, 0]
        self.vx = random.randint(min_speed_ball, max_speed_ball) * random.choice(temp)
        self.vy = random.randint(min_speed_ball, max_speed_ball) * random.choice(temp[0:-1])
        self.rect.x = pos_x
        self.rect.y = pos_y

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.collide_mask(self, player1):
            hit.play()
            self.vy = -self.vy
        if pygame.sprite.collide_mask(self, player2):
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
    if rule == 'right_d' and x > 5:
        obj.move(x + speed_player2, y)
    if rule == 'left_a' and x < width - 5:
        obj.move(x - speed_player2, y)
    if rule == 'left_s' and x > 5:
        obj.move(x - speed_player1, y)
    if rule == 'right_s' and x < width - 5:
        obj.move(x + speed_player1, y)


pygame.init()
m_left_s = False
m_right_s = False
m_left_a = False
m_right_d = False

Border(5, 5, 5, height - 5)
Border(width - 5, 5, width - 5, height - 5)

pygame.mixer.music.load("sound/fon.mp3")
hit = pygame.mixer.Sound("sound/hit.mp3")

backgraund = Backgraund()

player1 = Rocket1()
player2 = Rocket2()

clock = pygame.time.Clock()

pygame.mixer.music.play(-1)

running = True
move(player1, 'left_s')
move(player2, 'right_d')
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            Ball(width // 2, height // 2)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                m_left_s = True
            if event.key == pygame.K_RIGHT:
                m_right_s = True
            if event.key == pygame.K_a:
                m_left_a = True
            if event.key == pygame.K_d:
                m_right_d = True
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
        move(player1, 'left_s')
    elif m_right_s:
        move(player1, 'right_s')
    if m_left_a:
        move(player2, 'left_a')
    elif m_right_d:
        move(player2, 'right_d')
    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.flip()
    clock.tick(fps)
pygame.quit()
