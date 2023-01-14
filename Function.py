from data import width, height
import sys
import os
import pygame

screen = pygame.display.set_mode((width, height))


class Backgraund(pygame.sprite.Sprite):
    def __init__(self, sprites, image):
        super().__init__(sprites)
        self.image = image
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

    def __init__(self, sprite, image, pos):
        super().__init__(sprite)
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


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name1, name2):
    """
    Да, самый первобытный, но по факту почему-то альфа не работат
    (из-за изображений)
    """
    fullname = os.path.join('data', 'image', name1, name2)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def load_sound(name):
    fullname = os.path.join('data', 'sound', name)
    if not os.path.isfile(fullname):
        print(f"Файл с аудио '{fullname}' не найден")
        sys.exit()
    sound = pygame.mixer.Sound(fullname)
    return sound
