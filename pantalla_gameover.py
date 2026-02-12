import pygame
from utils import texto_puntuacion

class PantallaGameOver:
    def __init__(self, window, width, height):
        self.window = window
        self.width = width
        self.height = height

    def mostrar(self, score, width, height, ganaste=False):
        self.width = width
        self.height = height
        # Superficie traslúcida
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(204)
        overlay.fill((0, 0, 0))
        self.window.blit(overlay, (0, 0))
        
        if ganaste:
            titulo = '¡Misión completada!'
            color_titulo = (255, 215, 0) # Oro
        else:
            titulo = 'Juego terminado'
            color_titulo = (255, 0, 0) # Rojo
            
        texto_puntuacion(self.window, titulo, 60, self.width // 2, self.height // 2 - 100)
        texto_puntuacion(self.window, f'Puntuación final: {score}', 40, self.width // 2, self.height // 2)
        texto_puntuacion(self.window, 'Presiona R para volver a jugar', 30, self.width // 2, self.height // 2 + 100)
        pygame.display.flip()

    def esperar_reinicio(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        return True
