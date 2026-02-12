import pygame
import random


class Defensor(pygame.sprite.Sprite):
    """Pequeños enemigos que protegen al jefe"""
    
    def __init__(self, x, y, tipo_jefe=1):
        super().__init__()
        self.tipo_jefe = tipo_jefe
        
        # Cargar la imagen del jefe correspondiente y escalarla
        if tipo_jefe == 1:
            # Defensor del Jefe Monstruo
            img = pygame.image.load('imagenes/jefe1.png').convert_alpha()
            self.image = pygame.transform.scale(img, (120, 80))  # 50% del tamaño del jefe
            self.vida = 3
            self.velocidad = 1.8
        elif tipo_jefe == 2:
            # Defensor del Jefe Nave Nodriza
            img = pygame.image.load('imagenes/jefe2.png').convert_alpha()
            self.image = pygame.transform.scale(img, (120, 80))
            self.vida = 4
            self.velocidad = 2.2
        else:
            # Defensor del Jefe Robot
            img = pygame.image.load('imagenes/jefe3.png').convert_alpha()
            self.image = pygame.transform.scale(img, (120, 80))
            self.vida = 5
            self.velocidad = 2.5
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Asignar tipo de ataque aleatorio
        self.tipo_ataque = random.choice(['fuego', 'laser', 'espina'])
        
        # Patrón de movimiento
        self.direccion_x = random.choice([-1, 1])
        self.direccion_y = 1
        self.tiempo_cambio_direccion = pygame.time.get_ticks()
        self.tiempo_ultimo_disparo = pygame.time.get_ticks()
    
    
    
    def update(self, width, *args, **kwargs):
        # Movimiento errático
        ahora = pygame.time.get_ticks()
        
        # Cambiar dirección aleatoriamente
        if ahora - self.tiempo_cambio_direccion > random.randint(1000, 2000):
            self.direccion_x = random.choice([-1, 0, 1])
            self.tiempo_cambio_direccion = ahora
        
        # Mover
        self.rect.x += self.velocidad * self.direccion_x
        self.rect.y += self.velocidad * 0.5  # Moverse lentamente hacia abajo
        
        # Mantener dentro de los límites
        if self.rect.right >= width:
            self.rect.right = width
            self.direccion_x = -1
        if self.rect.left <= 0:
            self.rect.left = 0
            self.direccion_x = 1
        
        # Eliminar si sale de la pantalla por abajo
        # Obtener height de args si está disponible
        height = args[0] if args else None
        if height and self.rect.top > height:
            self.kill()
    
    
    def disparar(self, grupo_balas_enemigos):
        """Los defensores disparan ataques especiales ocasionalmente"""
        ahora = pygame.time.get_ticks()
        if ahora - self.tiempo_ultimo_disparo > random.randint(1500, 3000):
            # Usar ataques especiales del jefe
            from ataques_jefe import BolaFuego, LaserJefe, EspinaJefe
            
            if self.tipo_ataque == 'fuego':
                ataque = BolaFuego(self.rect.centerx, self.rect.bottom)
            elif self.tipo_ataque == 'laser':
                ataque = LaserJefe(self.rect.centerx, self.rect.bottom)
            else:  # espina
                ataque = EspinaJefe(self.rect.centerx, self.rect.bottom)
            
            grupo_balas_enemigos.add(ataque)
            self.tiempo_ultimo_disparo = ahora
