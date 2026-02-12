import pygame

class Explosion(pygame.sprite.Sprite):
    def __init__(self, position, explosion_list):
        super().__init__()
        self.image = explosion_list[0]
        img_scala = pygame.transform.scale(self.image, (20, 20))
        self.rect = img_scala.get_rect()
        self.rect.center = position
        self.time = pygame.time.get_ticks()
        self.velocidad_explo = 30
        self.frames = 0
        self.explosion_list = explosion_list

    def update(self, *args, **kwargs):
        tiempo = pygame.time.get_ticks()
        if tiempo - self.time > self.velocidad_explo:
            self.time = tiempo
            self.frames += 1
            if self.frames == len(self.explosion_list):
                self.kill()
            else:
                position = self.rect.center
                self.image = self.explosion_list[self.frames]
                self.rect = self.image.get_rect()
                self.rect.center = position
