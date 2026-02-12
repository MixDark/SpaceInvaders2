import pygame

class ExplosionCentrada(pygame.sprite.Sprite):
    """Explosión que siempre mantiene su centro en la posición especificada"""
    
    def __init__(self, position, explosion_list, tamano=(60, 60)):
        super().__init__()
        self.explosion_list = explosion_list
        self.tamano = tamano
        self.position = position  # Guardar posición permanentemente
        
        # Escalar primer frame
        self.image = pygame.transform.scale(explosion_list[0], tamano)
        self.rect = self.image.get_rect()
        self.rect.center = position
        
        self.time = pygame.time.get_ticks()
        self.velocidad_explo = 30
        self.frames = 0

    def update(self, *args, **kwargs):
        tiempo = pygame.time.get_ticks()
        if tiempo - self.time > self.velocidad_explo:
            self.time = tiempo
            self.frames += 1
            if self.frames == len(self.explosion_list):
                self.kill()
            else:
                # Escalar el nuevo frame y SIEMPRE recentrar
                self.image = pygame.transform.scale(self.explosion_list[self.frames], self.tamano)
                self.rect = self.image.get_rect()
                self.rect.center = self.position  # Mantener centrado en la posición original
