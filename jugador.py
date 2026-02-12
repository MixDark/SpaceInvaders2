import pygame

class Jugador(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.image = pygame.image.load('imagenes/A1.png').convert_alpha()
        pygame.display.set_icon(self.image)
        self.rect = self.image.get_rect()
        self.rect.centerx = width // 2
        self.rect.bottom = height
        self.velocidad_x = 0
        self.vidas = 3
        self.vida = 100
        self.ultimo_disparo = pygame.time.get_ticks()
        self.cadencia_disparo = 200 # Milisegundos entre disparos
        
        # Sistema de Poderes ACUMULABLES (con tiempo límite)
        self.poderes_activos = {} # { 'poder': tiempo_fin }
        self.arma_preferida = 'simple'
        self.velocidad_base = 5
        self.tiene_escudo = False
        self.invulnerable = False
        self.tiempo_invulnerable = 0

    def update(self, width, height=None):
        self.velocidad_x = 0
        keystate = pygame.key.get_pressed()
        vel = self.velocidad_base
        
        # Actualizar cadencia y velocidad según poderes acumulados
        ahora = pygame.time.get_ticks()
        
        # Limpiar poderes expirados
        expirados = [p for p, t in self.poderes_activos.items() if ahora > t]
        for p in expirados:
            del self.poderes_activos[p]
        
        # Aplicar efectos
        self.tiene_escudo = 'escudo' in self.poderes_activos
        self.cadencia_disparo = 100 if 'rapido' in self.poderes_activos else 200
        vel = 8 if 'rapido' in self.poderes_activos else self.velocidad_base

        # Gestión de invulnerabilidad
        if self.invulnerable and ahora > self.tiempo_invulnerable:
            self.invulnerable = False

        if keystate[pygame.K_LEFT]:
            self.velocidad_x = -vel
        elif keystate[pygame.K_RIGHT]:
            self.velocidad_x = vel
        self.rect.x += self.velocidad_x
        if self.rect.right > width:
            self.rect.x = width - self.rect.width
        if self.rect.left < 0:
            self.rect.left = 0
        # Permitir que la nave llegue hasta el borde inferior
        # Permitir que la nave llegue hasta el borde inferior
        if height is not None:
            if self.rect.bottom > height:
                self.rect.bottom = height

    def disparar(self, grupo_jugador, grupo_balas_jugador, laser_sonido, grupo_enemigos=None):
        ahora = pygame.time.get_ticks()
        if ahora - self.ultimo_disparo > self.cadencia_disparo:
            self.ultimo_disparo = ahora
            from balas import Balas
            
            # Determinar patrón de disparo: Priorizar el arma preferida si está activa
            patron = 'simple'
            if self.arma_preferida in self.poderes_activos:
                patron = self.arma_preferida
            else:
                # Si la preferida expiró, buscar cualquier otra arma disponible
                armas_disponibles = [p for p in self.poderes_activos.keys() if p in ['doble', 'triple', 'quintuple', 'laser', 'misil', 'teledirigido', 'ripple', 'mega']]
                if armas_disponibles:
                    patron = armas_disponibles[0] # Tomar la primera disponible
            
            if patron == 'simple':
                bala = Balas(self.rect.centerx, self.rect.top)
                grupo_jugador.add(bala)
                grupo_balas_jugador.add(bala)
            
            elif patron == 'doble':
                bala1 = Balas(self.rect.left + 10, self.rect.top)
                bala2 = Balas(self.rect.right - 10, self.rect.top)
                grupo_jugador.add(bala1, bala2); grupo_balas_jugador.add(bala1, bala2)
                
            elif patron == 'triple':
                bala1 = Balas(self.rect.centerx, self.rect.top)
                bala2 = Balas(self.rect.left, self.rect.top + 10)
                bala3 = Balas(self.rect.right, self.rect.top + 10)
                grupo_jugador.add(bala1, bala2, bala3); grupo_balas_jugador.add(bala1, bala2, bala3)
            
            elif patron == 'quintuple':
                for i in range(-2, 3):
                    bala = Balas(self.rect.centerx + (i * 15), self.rect.top + (abs(i) * 5))
                    grupo_jugador.add(bala); grupo_balas_jugador.add(bala)
            
            elif patron == 'laser':
                laser = Balas(self.rect.centerx, self.rect.top)
                laser.image = pygame.Surface((80, 500), pygame.SRCALPHA)
                for i in range(5):
                    x_p = 8 + (i * 16)
                    pygame.draw.line(laser.image, (255, 0, 255), (x_p, 0), (x_p, 500), 5)
                    pygame.draw.line(laser.image, (255, 255, 255), (x_p, 0), (x_p, 500), 1)
                laser.rect = laser.image.get_rect(centerx=self.rect.centerx, bottom=self.rect.top)
                laser.velocidad = -25
                grupo_jugador.add(laser); grupo_balas_jugador.add(laser)
            
            elif patron == 'misil':
                bala = Balas(self.rect.centerx, self.rect.top)
                bala.image = pygame.image.load('imagenes/misil2.png').convert_alpha()
                bala.image = pygame.transform.scale(bala.image, (30, 70))
                bala.rect = bala.image.get_rect(centerx=self.rect.centerx, bottom=self.rect.top)
                bala.velocidad = -12
                grupo_jugador.add(bala); grupo_balas_jugador.add(bala)

            elif patron == 'teledirigido':
                from balas import MisilTeledirigido
                if grupo_enemigos:
                    bala = MisilTeledirigido(self.rect.centerx, self.rect.top, grupo_enemigos)
                    grupo_jugador.add(bala); grupo_balas_jugador.add(bala)
                else:
                    # Fallback a simple si no hay grupo
                    bala = Balas(self.rect.centerx, self.rect.top)
                    grupo_jugador.add(bala); grupo_balas_jugador.add(bala)

            elif patron == 'ripple':
                from balas import RayoRipple
                bala = RayoRipple(self.rect.centerx, self.rect.top)
                grupo_jugador.add(bala); grupo_balas_jugador.add(bala)

            elif patron == 'mega':
                mega = Balas(self.rect.centerx, self.rect.top)
                mega.image = pygame.Surface((200, 600), pygame.SRCALPHA)
                # Dibujar un rayo masivo azul/blanco
                pygame.draw.rect(mega.image, (0, 0, 255, 100), (0, 0, 200, 600))
                pygame.draw.rect(mega.image, (255, 255, 255, 200), (50, 0, 100, 600))
                mega.rect = mega.image.get_rect(centerx=self.rect.centerx, bottom=self.rect.top)
                mega.velocidad = -20
                grupo_jugador.add(mega); grupo_balas_jugador.add(mega)
                
            laser_sonido.play()
            
    def dibujar_escudo(self, window):
        if self.tiene_escudo:
            # Dibujar un círculo traslúcido cian alrededor de la nave
            shield_surf = pygame.Surface((self.rect.width + 40, self.rect.height + 40), pygame.SRCALPHA)
            pygame.draw.circle(shield_surf, (0, 255, 255, 120), (self.rect.width//2 + 20, self.rect.height//2 + 20), (self.rect.width//2 + 15), 3)
            window.blit(shield_surf, (self.rect.centerx - (self.rect.width//2 + 20), self.rect.centery - (self.rect.height//2 + 20)))
