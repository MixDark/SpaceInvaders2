import pygame
import random

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Tipos: 'misil', 'escudo', 'vida', 'bomba'
        self.tipo = random.choice(['misil', 'escudo', 'vida', 'bomba'])
        
        # Colores según el tipo
        self.color = {
            'misil': (255, 165, 0),  # Naranja
            'escudo': (0, 255, 255), # Cian/Escudo
            'vida': (255, 0, 0),      # Rojo
            'bomba': (128, 0, 128)    # Púrpura (Bomba Atómica)
        }[self.tipo]
        
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        # Dibujar forma circular para que parezca más un ícono de poder
        pygame.draw.circle(self.image, self.color, (15, 15), 14)
        pygame.draw.circle(self.image, (255, 255, 255), (15, 15), 14, 2)
        
        # Agregar un brillo sutil
        pygame.draw.circle(self.image, (255, 255, 255), (10, 10), 4)
        
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.velocidad_y = random.uniform(2, 4)  # Velocidad vertical variada
        self.velocidad_x = random.uniform(-1.5, 1.5)  # Velocidad horizontal para evitar sobreposición

    def update(self):
        # Movimiento diagonal para dispersar
        self.rect.y += self.velocidad_y
        self.rect.x += self.velocidad_x
        
        # Obtener dimensiones de pantalla
        screen = pygame.display.get_surface()
        if screen:
            width = screen.get_width()
            height = screen.get_height()
            
            # Rebotar en los bordes laterales
            if self.rect.left <= 0:
                self.rect.left = 0
                self.velocidad_x *= -1
            elif self.rect.right >= width:
                self.rect.right = width
                self.velocidad_x *= -1
                
            # Eliminar si sale de la pantalla por abajo
            if self.rect.top > height:
                self.kill()
        else:
            if self.rect.top > 800:
                self.kill()
