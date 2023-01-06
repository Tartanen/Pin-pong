import pygame

from terminate import terminate
from load_image import load_image

fps = 10
width = 640
height = 1024
is_running = False
all_sprites = pygame.sprite.Group()

menu = {}
for i in range(1, 72):
    menu[i] = load_image(f'Anime\{i}.jpg')
    pygame.transform.scale(menu[i], (width, height))
print(menu)


class Backgraund(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.frame = 1
        self.image = menu[self.frame]
        self.rect = self.image.get_rect()

    def update(self):
        self.frame = self.frame % 71
        self.frame += 1
        self.image = menu[self.frame]
        screen.blit(self.image, self.rect)


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



def start_screen():
    running = True
    Backgraund()
    Menu()
    start = Button((load_image('start_button.png'), load_image('start_button_press.png')), (width / 2, height // 5 * 2))
    option = Button((load_image('eturn_button.png'), load_image('eturn_button_press.png')), (width / 2, height // 5 * 3))
    close = Button((load_image('exit_button.png'), load_image('exit_button_press.png')), (width / 2, height // 5 * 4))
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
        start.checkguad(pygame.mouse.get_pos())
        option.checkguad(pygame.mouse.get_pos())
        close.checkguad(pygame.mouse.get_pos())
        all_sprites.draw(screen)
        all_sprites.update()
        pygame.display.update()
        clock.tick(fps)
    terminate()

clock = pygame.time.Clock()
pygame.init()
screen = pygame.display.set_mode((width, height))


