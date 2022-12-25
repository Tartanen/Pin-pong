import pygame
import os
import sys
import random
from data import speed_ball, speed_player1, speed_player2, max_speed_player1, max_speed_player2

radius = 50
fps = 50
width = 400
height = 550

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
pygame.display.set_caption('Пин-понг')

player = None
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

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Rocket1.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.bottom = height


class Rocket2(pygame.sprite.Sprite):
    image = load_image('rocket2.png')

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Rocket2.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.bottom = height


class Ball(pygame.sprite.Sprite):
    image = load_image("ball.png")

    def __init__(self, pos):
        super().__init__(all_sprites)
        self.image = Ball.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.vx = random.randint(-(speed_ball), speed_ball)
        self.vy = random.randrange(-(speed_ball), speed_ball)
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


pygame.init()

Border(5, 5, 5, height - 5)
Border(width - 5, 5, width - 5, height - 5)

pygame.mixer.music.load("sound/fon.mp3")
hit = pygame.mixer.Sound("sound/hit.mp3")

Player1 = Rocket1()
Player2 = Rocket2()
screen.fill('black')

clock = pygame.time.Clock()
running = True

pygame.mixer.music.play(-1)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            Ball(event.pos)
    screen.fill('black')
    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.flip()
    clock.tick(fps)
pygame.quit()
