import pygame
import random

class BolaFuego(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('imagenes/fuego.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.y = y
        self.velocidad_y = 6
    def update(self, *args, **kwargs):
        self.rect.y += self.velocidad_y
        screen = pygame.display.get_surface()
        height = screen.get_height() if screen else 800
        if self.rect.top > height:
            self.kill()

class LaserJefe(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('imagenes/laser.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.y = y
        self.velocidad_y = 12
    def update(self, *args, **kwargs):
        self.rect.y += self.velocidad_y
        screen = pygame.display.get_surface()
        height = screen.get_height() if screen else 800
        if self.rect.top > height:
            self.kill()

class EspinaJefe(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('imagenes/espina.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.y = y
        self.velocidad_y = 8
    def update(self, *args, **kwargs):
        self.rect.y += self.velocidad_y
        screen = pygame.display.get_surface()
        height = screen.get_height() if screen else 800
        if self.rect.top > height:
            self.kill()
