import random

import pygame

from data import max_speed_ball, min_speed_ball, speed_player1, speed_player2
from terminate import terminate
from load_image import load_image
from load_sound import load_sound

fps = 60
width = 640
height = 1024

screen = pygame.display.set_mode((width, height))
pygame.init()

horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
back_sprites = pygame.sprite.Group()
ball_sprites = pygame.sprite.Group()

clock = pygame.time.Clock()

teleports = False
wins = False


def move(obj, rule, rep):
    x, y = obj.pos
    if rule == 'right_d' and x + obj.image.get_rect().size[0] < width - 5:
        for j in range(rep):
            obj.move(x + speed_player2, y)
    if rule == 'left_a' and x > 5:
        for j in range(rep):
            obj.move(x - speed_player2, y)
    if rule == 'left_s' and x > 5:
        for j in range(rep):
            obj.move(x - speed_player1, y)
    if rule == 'right_s' and x + obj.image.get_rect().size[0] < width - 5:
        for j in range(rep):
            obj.move(x + speed_player1, y)
    if rule == 'up' and y - obj.image.get_rect().size[1] < 30:
        for j in range(rep):
            obj.move(x, y - speed_player1)
    if rule == 'down' and y + obj.image.get_rect().size[1] < width - 20:
        for j in range(rep):
            obj.move(x, y + speed_player1)


class Rocket1(pygame.sprite.Sprite):
    image = load_image('ракетка 1 (1).png')

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Rocket1.image
        self.pos_x = width / 2 - self.image.get_rect().size[0] / 2
        self.pos_y = height - self.image.get_rect().size[-1] - 30
        self.pos = self.pos_x, self.pos_y
        self.rect = self.image.get_rect(center=self.pos)
        self.mask = pygame.mask.from_surface(self.image)

    def move(self, x, y):
        self.pos = x, y
        self.rect = self.image.get_rect().move(x, y)

    def tp(self):
        self.pos = self.pos_x, self.pos_y
        self.rect = self.image.get_rect(center=self.pos)


class Rocket2(pygame.sprite.Sprite):
    image = load_image('ракетка 2 (1).png')

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Rocket2.image
        self.pos_x = width / 2 - self.image.get_rect().size[0] / 2
        self.pos_y = 15
        self.pos = self.pos_x, self.pos_y
        self.rect = self.image.get_rect(center=self.pos)
        self.mask = pygame.mask.from_surface(self.image)

    def move(self, x, y):
        self.pos = x, y
        self.rect = self.image.get_rect().move(x, y)

    def tp(self):
        self.pos = self.pos_x, self.pos_y
        self.rect = self.image.get_rect(center=self.pos)


class Score(pygame.sprite.Sprite):
    def __init__(self, pos, nab, num):
        super().__init__(all_sprites)
        self.score = 0
        self.pos = pos
        self.nab = nab
        self.num = num
        self.image = self.nab[self.score]
        self.rect = self.image.get_rect(center=self.pos)

    def update(self):
        screen.blit(self.image, self.rect)
        self.image = self.nab[self.score]
        if self.score == 11:
            pygame.mixer.stop()
            global teleports, wins
            if self.num == 1:
                wins = True
            teleports = True
            win.play()

    def score_update(self, tp):
        if self.score == 0:
            self.score += 10
        else:
            self.score += tp

    def clear_score(self):
        self.score += 1
        self.score /= self.score
        self.score -= 1


class Ball(pygame.sprite.Sprite):
    image = load_image("ball.png")

    def __init__(self, pos_x, pos_y):
        super().__init__(ball_sprites)
        self.image = Ball.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        temp = [1, -1, 0]
        self.vx = random.randint(min_speed_ball, max_speed_ball) * random.choice(temp)
        self.vy = random.randint(min_speed_ball, max_speed_ball) * random.choice(temp[0:-1])
        self.rect.x = pos_x
        self.rect.y = pos_y

    def update(self):
        temp1 = 0
        temp2 = 0
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
            if self.rect[1] > (height // 2):
                temp1 += 1
            if self.rect[1] < (height // 2):
                temp2 += 1
            player11.score_update(temp1)
            player22.score_update(temp2)
            clear_by_ball()


def clear_by_ball():
    for sprite in ball_sprites:
        sprite.kill()


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


def game(ret):
    if ret:
        global teleports, wins
        teleports = False
        wins = False
        player1.tp()
        player2.tp()
        player11.clear_score()
        player22.clear_score()

    m_left_s = False
    m_right_s = False
    m_left_a = False
    m_right_d = False

    clock = pygame.time.Clock()

    Backgraund()

    Border(5, 5, width - 5, 5)
    Border(5, height - 5, width - 5, height - 5)
    Border(5, 5, 5, height - 5)
    Border(width - 5, 5, width - 5, height - 5)
    pause = Button((load_image('pause_btn.png'), load_image('pause_btn_pr.png')), (width - 30, height // 2))

    # pygame.mixer.music.load("data/sound/fon.mp3")#Фоновая музака
    # pygame.mixer.music.play(-1)#
    # pygame.mixer.music.set_volume(0.3)#

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 'pause', False
                if event.key == pygame.K_LEFT:
                    m_left_s = True
                if event.key == pygame.K_RIGHT:
                    m_right_s = True
                if event.key == pygame.K_a:
                    m_left_a = True
                if event.key == pygame.K_d:
                    m_right_d = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_g:
                    Ball(width // 2, height // 2)
                if event.key == pygame.K_LEFT:
                    m_left_s = False
                if event.key == pygame.K_RIGHT:
                    m_right_s = False
                if event.key == pygame.K_a:
                    m_left_a = False
                if event.key == pygame.K_d:
                    m_right_d = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pause.checkpress(event.pos):
                    return 'pause', False
        if m_left_s:
            move(player1, 'left_s', 1)
        if m_right_s:
            move(player1, 'right_s', 1)
        if m_left_a:
            move(player2, 'left_a', 1)
        if m_right_d:
            move(player2, 'right_d', 1)
        if teleports:
            return 'win', wins
        pause.checkguad(pygame.mouse.get_pos())
        back_sprites.draw(screen)
        back_sprites.update()
        all_sprites.draw(screen)
        all_sprites.update()
        ball_sprites.draw(screen)
        ball_sprites.update()
        pygame.display.flip()
        clock.tick(fps)
    terminate()


numb_red = {}
for i in range(0, 12):
    numb_red[i] = load_image(f'number\{i}_син.png')
numb_blue = {}
for i in range(0, 12):
    numb_blue[i] = load_image(f'number\{i}_красн.png')
hit = load_sound("hit.mp3")
loss = load_sound("loss1.mp3")
win = load_sound('win.mp3')
player11 = Score((30, height // 2 - 30), numb_red, 1)
player22 = Score((30, height // 2 + 30), numb_blue, 0)

player1 = Rocket1()
player2 = Rocket2()
