import pygame
import random

class Balas(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('imagenes/B2.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.y = y
        self.velocidad = -18

    def update(self, *args, **kwargs):
        self.rect.y += self.velocidad
        if self.rect.bottom < 0:
            self.kill()

class MisilTeledirigido(Balas):
    def __init__(self, x, y, grupo_enemigos):
        super().__init__(x, y)
        self.image = pygame.image.load('imagenes/misil_guiado.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 70))
        self.rect = self.image.get_rect(centerx=x, bottom=y)
        self.grupo_enemigos = grupo_enemigos
        self.velocidad = -10
        self.objetivo = None

    def update(self, *args, **kwargs):
        if not self.objetivo or not self.objetivo.alive():
            # Buscar el enemigo más cercano
            enemigos = self.grupo_enemigos.sprites()
            if enemigos:
                self.objetivo = min(enemigos, key=lambda e: ((self.rect.x - e.rect.x)**2 + (self.rect.y - e.rect.y)**2))
        
        if self.objetivo:
            if self.rect.centerx < self.objetivo.rect.centerx:
                self.rect.x += 3
            elif self.rect.centerx > self.objetivo.rect.centerx:
                self.rect.x -= 3
        
        self.rect.y += self.velocidad
        if self.rect.bottom < 0:
            self.kill()

class RayoRipple(Balas):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.size = 20
        self.image_original = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        pygame.draw.circle(self.image_original, (0, 255, 255), (self.size//2, self.size//2), self.size//2, 2)
        self.image = self.image_original
        self.rect = self.image.get_rect(centerx=x, bottom=y)
        self.velocidad = -12

    def update(self, *args, **kwargs):
        self.size += 4 # Expandir el anillo
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (0, 255, 255), (self.size//2, self.size//2), self.size//2, 3)
        old_center = self.rect.center
        self.rect = self.image.get_rect(center=old_center)
        self.rect.y += self.velocidad
        if self.rect.bottom < 0 or self.size > 200:
            self.kill()

class BalasEnemigos(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('imagenes/B1.png').convert_alpha()
        self.image = pygame.transform.rotate(self.image, 180)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.y = y # Usar la posición y del enemigo
        self.velocidad_y = 4

    def update(self, *args, **kwargs):
        self.rect.y += self.velocidad_y
        # Obtener la superficie de la pantalla para saber el límite inferior
        screen = pygame.display.get_surface()
        height = screen.get_height() if screen else 800
        if self.rect.top > height:
            self.kill()
