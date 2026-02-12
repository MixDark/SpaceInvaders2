import pygame
import random

class Enemigos(pygame.sprite.Sprite):
    def __init__(self, width, nivel=1):
        super().__init__()
        self.image = pygame.image.load('imagenes/E1.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(1, width - 50)
        self.rect.y = random.randrange(10, 100)
        self.velocidad_x = random.choice([-3, 3])
        self.velocidad_y = 10
        # Los enemigos se vuelven más resistentes con cada nivel (1 impacto adicional cada 2 niveles)
        self.vida = 1 + (nivel // 3)
        self.nivel = nivel

    def update(self, width, *args, **kwargs):
        self.rect.x += self.velocidad_x
        if self.rect.right > width:
            self.rect.x = width - self.rect.width
            self.velocidad_x *= -1
            self.rect.y += self.velocidad_y
        if self.rect.left < 0:
            self.rect.left = 0
            self.velocidad_x *= -1
            self.rect.y += self.velocidad_y
        
        screen = pygame.display.get_surface()
        height = screen.get_height() if screen else 800
        if self.rect.bottom > height - 150:
            self.rect.bottom = height - 150

    def disparar_enemigos(self, grupo_jugador, grupo_balas_enemigos, laser_sonido):
        from balas import BalasEnemigos
        bala = BalasEnemigos(self.rect.centerx, self.rect.bottom)
        grupo_jugador.add(bala)
        grupo_balas_enemigos.add(bala)
        laser_sonido.play()


    def spawn_escoltas(self, grupo_enemigos, width, nivel_actual):
        ahora = pygame.time.get_ticks()
        # Solo invoca naves si hay pocas en pantalla (máximo 10 escoltas a la vez)
        if ahora - self.ultimo_spawn > self.cadencia_spawn and len(grupo_enemigos) < 12:
            self.ultimo_spawn = ahora
            for i in range(3): # Invoca de 3 en 3
                escolta = Enemigos(width, nivel_actual)
                escolta.rect.centerx = self.rect.centerx + random.randint(-100, 100)
                escolta.rect.top = self.rect.bottom
                escolta.velocidad_x = random.choice([-5, 5])
                escolta.vida = 2 # Escoltas un poco más resistentes
                grupo_enemigos.add(escolta)

    def disparar(self, grupo_jugador, grupo_balas_enemigos, laser_sonido):
        ahora = pygame.time.get_ticks()
        if ahora - self.ultimo_disparo > self.cadencia:
            self.ultimo_disparo = ahora
            from balas import BalasEnemigos
            # El jefe dispara 5 balas en abanico para máxima dificultad
            for offset in [-120, -60, 0, 60, 120]:
                bala = BalasEnemigos(self.rect.centerx + offset, self.rect.bottom)
                bala.image = pygame.transform.scale(bala.image, (25, 50))
                bala.rect = bala.image.get_rect(center=bala.rect.center)
                grupo_jugador.add(bala)
                grupo_balas_enemigos.add(bala)
            laser_sonido.play()
