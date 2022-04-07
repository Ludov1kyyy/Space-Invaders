import pygame
from setup import WIDTH, HEIGHT, WHITE_COLOR
from random import randint

pygame.init()

class CRT:
    def __init__(self):
        self.tv = pygame.image.load("../graphics/tv.png").convert_alpha()
        self.tv = pygame.transform.scale(self.tv, (WIDTH, HEIGHT))

        line_h = 3
        amount = WIDTH // line_h

        for line in range(amount):
            pos_y = line * line_h
            pygame.draw.line(self.tv, "black", (0, pos_y), (WIDTH, pos_y))

    def draw(self, win):
        self.tv.set_alpha(randint(75, 90))
        win.blit(self.tv, (0, 0))

FONT = pygame.font.Font("../font/Pixeled.ttf", 20)

class Text:
    def __init__(self, info, pos, point="center"):
        win = pygame.display.get_surface()

        info_surf = FONT.render(str(info), True, WHITE_COLOR)

        if point == "center":
            info_rect = info_surf.get_rect(center = pos)
        else:
            info_rect = info_surf.get_rect(topleft = pos)

        win.blit(info_surf, info_rect)

class Audio:
    def __init__(self, path):
        self.audio = pygame.mixer.Sound(path)

    def play(self, loop=0, volume=0.3):
        self.audio.set_volume(volume)
        self.audio.play(loops = loop)
