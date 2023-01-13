import random
import pygame

from data import max_speed_ball, min_speed_ball, speed_player1, speed_player2
from data import width, height, fps, max_speed_player1, max_speed_player2
from Function import terminate
from load_image import load_image
from load_sound import load_sound

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


def move(obj, rule, koef):
    x, y = obj.pos
    if rule == 'right_d' and x + obj.image.get_rect().size[0] < width - 5:
        obj.move(round(x + speed_player2 * koef), y)
    if rule == 'left_a' and x > 5:
        obj.move(round(x - speed_player2 * koef), y)
    if rule == 'left_s' and x > 5:
        obj.move(round(x - speed_player1 * koef), y)
    if rule == 'right_s' and x + obj.image.get_rect().size[0] < width - 5:
        obj.move(round(x + speed_player1 * koef), y)


class Rocket(pygame.sprite.Sprite):
    """
    Класс ракеток. Проще только класс фона и границ.
    Из интересного:
    1. Помнит центр и откуда ничинать движения для рестарта игры
    2. Задаёт коллизию для ракетки чтобы мячик отстукивался в различном
    направлении
    """

    def __init__(self, image, pos):
        super().__init__(all_sprites)
        self.image = image
        self.pos_x = pos[0]
        self.pos_y = pos[-1]
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
    """
        Класс счёта. Тут у нас ведётся подсчёт результатов игры!
        Из интересного:
        1. Каждый счёт загружается индивидуально (это доп. нагрузка на
        пк, но есть возможность кастомизации)
        2. Реализация цикла получилась через глобалки (грустненько), но
        так оно работает, а не выпадает в ошибку
        """

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

    def score_update(self, tp):
        self.score += tp

    def check_score(self):
        if self.score == 11:
            winer = False
            pygame.mixer.stop()
            win.play()
            if self.num == 1:
                winer = True
            return True, winer
        return False, False

    def clear_score(self):
        self.score += 1
        self.score /= self.score
        self.score -= 1


class Ball(pygame.sprite.Sprite):
    """
    Класс мяча. Можно сказать сердце всего кода т.к. вся физика полётов
    и система побед проигрышей считается здесь!
    Из интересного:
    1. после столкновение с ракеткой движение по оси У и Х
    пересчитывается заново для интереса игры
    2. Тут есть система очистки поля от лишних шаров
    (нажмите G пару раз и посмотрите)
    ну и звуки ударов, вылетов за границы поля тоже
    """
    image = load_image('backstage', "ball.png")

    def __init__(self, pos_x, pos_y):
        super().__init__(ball_sprites)
        self.image = Ball.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        temp = [1, -1, 0]
        self.vx = (random.randint(min_speed_ball, max_speed_ball)
                   * random.choice(temp))
        self.vy = (random.randint(min_speed_ball, max_speed_ball)
                   * random.choice(temp[0:-1]))
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


# Удаление шариков (+ оптимизация и решение кучи багов)
def clear_by_ball():
    for sprite in ball_sprites:
        sprite.kill()


class Border(pygame.sprite.Sprite):
    """Это класс выставления границ поля (собственно ничего нового)"""

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
    """Это класс изображения поля (собственно ничего нового)"""
    im = load_image('backstage', "space-bck1.png")

    def __init__(self):
        super().__init__(back_sprites)
        self.image = Backgraund.im
        self.rect = self.image.get_rect()


class Button(pygame.sprite.Sprite):
    """
    класс батон
    класс в котором создаются кнопки и присваивается вещи:
    1. нажатия - мега вещь с помощью которой получется
    переключаться между внутренними окнами
    2. есть ли курсор в поле - отследить и указать что выбрана
    кнопка не от взлома Пентагона
    """

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


# Цикл игры
def game(ret):
    # delay - в секундах
    delay = 3
    if ret:
        clear_by_ball()
        player1.tp()
        player2.tp()
        player11.clear_score()
        player22.clear_score()

    m_left_s = False
    m_right_s = False
    m_left_a = False
    m_right_d = False
    lshift = False
    rshift = False
    rrshift = 1
    llshift = 1

    clock = pygame.time.Clock()

    Backgraund()

    Border(5, 5, width - 5, 5)
    Border(5, height - 5, width - 5, height - 5)
    Border(5, 5, 5, height - 5)
    Border(width - 5, 5, width - 5, height - 5)
    pause = Button((load_image('button', 'pause_btn.png'),
                    load_image('button', 'pause_btn_pr.png')),
                   (width - 30, height // 2))

    running = True
    delay_tp = fps * delay

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 'pause', False
                if event.key == pygame.K_RSHIFT:
                    rshift = True
                if event.key == pygame.K_LEFT:
                    m_left_s = True
                if event.key == pygame.K_RIGHT:
                    m_right_s = True
                if event.key == pygame.K_LSHIFT:
                    lshift = True
                if event.key == pygame.K_a:
                    m_left_a = True
                if event.key == pygame.K_d:
                    m_right_d = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LSHIFT:
                    lshift = False
                if event.key == pygame.K_RSHIFT:
                    rshift = False
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
        if lshift:
            llshift = max_speed_player1
        if rshift:
            rrshift = max_speed_player2
        if m_left_s:
            move(player1, 'left_s', rrshift)
        if m_right_s:
            move(player1, 'right_s', rrshift)
        if m_left_a:
            move(player2, 'left_a', llshift)
        if m_right_d:
            move(player2, 'right_d', llshift)
        if player11.check_score()[0]:
            return 'win', player11.check_score()[1]
        if player22.check_score()[0]:
            return 'win', player22.check_score()[1]
        if len(ball_sprites) == 0:
            if delay_tp != 0:
                delay_tp -= 1
            else:
                delay_tp = fps * delay
                Ball(width // 2, height // 2)
        rrshift = 1
        llshift = 1
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
    numb_red[i] = load_image('number', f'{i}_красн.png')
numb_blue = {}
for i in range(0, 12):
    numb_blue[i] = load_image('number', f'{i}_син.png')
hit = load_sound("hit.mp3")
loss = load_sound("loss1.mp3")
win = load_sound('win.mp3')
player11 = Score((30, height // 2 - 30), numb_red, 1)
player22 = Score((30, height // 2 + 30), numb_blue, 0)

player1 = Rocket(load_image('backstage', 'ракетка 1 (1).png'),
                 (width // 2, height - 45))
player2 = Rocket(load_image('backstage', 'ракетка 2 (1).png'),
                 (width // 2, 15))
