import sys
import os
import pygame
from main im
def menu():

    title = pygame.image.load(path.join(img_dir, "The_Lonely_Shooter.png")).convert_alpha()
    title = pygame.transform.scale(title, (WINDOWWIDTH, 81 * 2))
    background = pygame.image.load('images/stars_bg.jpeg').convert()
    background_rect = background.get_rect()

    arrow_keys = pygame.image.load(path.join(img_dir, 'arrowkeys.png')).convert_alpha()
    arrow_keys = pygame.transform.scale(arrow_keys, (150, 85))
    spacebar = pygame.image.load(path.join(img_dir, 'spacebar.png')).convert_alpha()
    spacebar = pygame.transform.scale(spacebar, (150, 50))

    DISPLAYSURF.blit(background, background_rect)
    DISPLAYSURF.blit(title, (0, 20))
    DISPLAYSURF.blit(arrow_keys, (225, 400))
    DISPLAYSURF.blit(spacebar, (225, 500))
    pygame.draw.rect(DISPLAYSURF, GREENYELLOW, (80, 294, 321, 35))
    pygame.draw.rect(DISPLAYSURF, GREENYELLOW, (120, 345, 240, 35))
    draw_text(DISPLAYSURF, "PRESS [ENTER] TO BEGIN", 35, WINDOWWIDTH / 2, WINDOWHEIGHT / 2, DARKGREY)
    draw_text(DISPLAYSURF, "PRESS [Q] TO QUIT", 35, WINDOWWIDTH / 2, (WINDOWHEIGHT / 2) + 50, DARKGREY)

    # game instructions
    pygame.draw.rect(DISPLAYSURF, GREENYELLOW, (50, 430, 100, 35))
    pygame.draw.rect(DISPLAYSURF, GREENYELLOW, (50, 510, 100, 35))
    draw_text(DISPLAYSURF, "MOVE:", 35, 100, 436, DARKGREY)
    draw_text(DISPLAYSURF, "SHOOT:", 35, 101, 516, DARKGREY)

    pygame.display.update()

    while True:
        event = pygame.event.poll()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                break
            elif event.key == pygame.K_q:
                pygame.quit()
                sys.exit()
        elif event.type == QUIT:
            pygame.quit()
            sys.exit() 