import pygame
import random


class Jefe(pygame.sprite.Sprite):
    def disparar(self, grupo_jugador, grupo_balas_enemigos, laser_sonido):
        self.ataque_especial(grupo_balas_enemigos)

    def spawn_escoltas(self, grupo_enemigos, width, nivel_actual):
        """Generar pequeños defensores que protegen al jefe"""
        from defensor import Defensor
        
        ahora = pygame.time.get_ticks()
        
        # Contar cuántos defensores hay actualmente
        defensores_actuales = sum(1 for enemigo in grupo_enemigos if isinstance(enemigo, Defensor))
        
        # Generar nuevos defensores si no hemos alcanzado el máximo
        if defensores_actuales < self.max_defensores:
            # Intervalo de spawn más corto para generar más defensores
            intervalo = 4000 if self.tipo == 1 else (3000 if self.tipo == 2 else 2500)
            
            if ahora - self.tiempo_ultimo_spawn_defensor > intervalo:
                # Posición MUY CERCA del jefe
                offset_x = random.choice([-60, -30, 30, 60])
                offset_y = random.choice([20, 40, 60])
                
                defensor = Defensor(
                    self.rect.centerx + offset_x,
                    self.rect.centery + offset_y,
                    tipo_jefe=self.tipo
                )
                grupo_enemigos.add(defensor)
                self.tiempo_ultimo_spawn_defensor = ahora
    
    def _crear_frames_animacion(self):
        """Crear frames de animación para el jefe usando transformaciones sutiles"""
        if self.tipo == 1:
            # JEFE MONSTRUO: Animación de respiración (escala sutil)
            for i in range(4):
                # Escala que pulsa (respiración) - muy sutil
                escala = 1.0 + (i * 0.015) if i < 2 else 1.0 + ((3 - i) * 0.015)
                
                # Obtener dimensiones originales
                w_original, h_original = self.image_base.get_size()
                nuevo_w = int(w_original * escala)
                nuevo_h = int(h_original * escala)
                
                # Escalar imagen
                frame = pygame.transform.scale(self.image_base, (nuevo_w, nuevo_h))
                
                self.frames.append(frame)
        elif self.tipo == 2:
            # JEFE NAVE NODRIZA: Animación muy sutil
            for i in range(4):
                # Escala muy ligera
                escala = 1.0 + (i * 0.01) if i < 2 else 1.0 + ((3 - i) * 0.01)
                w_original, h_original = self.image_base.get_size()
                nuevo_w = int(w_original * escala)
                nuevo_h = int(h_original * escala)
                frame = pygame.transform.scale(self.image_base, (nuevo_w, nuevo_h))
                self.frames.append(frame)
        elif self.tipo == 3:
            # JEFE ROBOT: Animación muy sutil
            for i in range(4):
                escala = 1.0 + (i * 0.01) if i < 2 else 1.0 + ((3 - i) * 0.01)
                w_original, h_original = self.image_base.get_size()
                nuevo_w = int(w_original * escala)
                nuevo_h = int(h_original * escala)
                frame = pygame.transform.scale(self.image_base, (nuevo_w, nuevo_h))
                self.frames.append(frame)
        else:
            # Fallback: usar imagen base
            self.frames.append(self.image_base.copy())

    def __init__(self, width, tipo=1):
        super().__init__()
        # tipo: 1 = jefe nivel 11, 2 = jefe nivel 21, 3 = jefe nivel 31
        self.tipo = tipo
        if tipo == 3:
            img = pygame.image.load('imagenes/jefe3.png').convert_alpha()
            self.image_base = pygame.transform.scale(img, (240, 160))
            self.vida = 400 * 5 * 2  # 5 veces más que antes, y el doble respecto al anterior
            self.velocidad_x = 7
        elif tipo == 2:
            img = pygame.image.load('imagenes/jefe2.png').convert_alpha()
            self.image_base = pygame.transform.scale(img, (240, 160))
            self.vida = 300 * 5  # 5 veces más que antes
            self.velocidad_x = 6
        else:
            img = pygame.image.load('imagenes/jefe1.png').convert_alpha()
            self.image_base = pygame.transform.scale(img, (240, 160))
            self.vida = 200 * 5  # 5 veces más que antes
            self.velocidad_x = 4
        
        # Sistema de animación
        self.frames = []
        self.frame_actual = 0
        self.tiempo_animacion = pygame.time.get_ticks()
        self.velocidad_animacion = 150  # Milisegundos entre frames
        
        # Crear frames de animación
        self._crear_frames_animacion()
        self.image = self.frames[0] if self.frames else self.image_base
        
        self.vida_max = self.vida  # Atributo para la barra de vida
        self.rect = self.image.get_rect()
        self.rect.centerx = width // 2
        self.rect.y = 160  # Bajamos más el jefe para dejar espacio al HUD de dos filas
        self.velocidad_y = 0
        self.direccion = 1
        self.tiempo_ultimo_disparo = pygame.time.get_ticks()
        self.tiempo_ultimo_ataque = pygame.time.get_ticks()
        self.tiempo_ultimo_spawn_defensor = pygame.time.get_ticks()
        self.max_defensores = 3 if tipo == 1 else (4 if tipo == 2 else 5)  # Reducido por tamaño aumentado

    def ataque_especial(self, grupo_balas_enemigos):
        ahora = pygame.time.get_ticks()
        if self.tipo == 3:
            from balas import BalasEnemigos
            # Jefe final: ataque múltiple, ráfagas y balas rápidas
            if ahora - self.tiempo_ultimo_ataque > 500:
                for dx in [-60, -30, 0, 30, 60]:
                    bala = BalasEnemigos(self.rect.centerx + dx, self.rect.bottom)
                    grupo_balas_enemigos.add(bala)
                self.tiempo_ultimo_ataque = ahora
        elif self.tipo == 2:
            from balas import BalasEnemigos
            # Jefe intermedio: ataque triple
            if ahora - self.tiempo_ultimo_ataque > 800:
                for dx in [-40, 0, 40]:
                    bala = BalasEnemigos(self.rect.centerx + dx, self.rect.bottom)
                    grupo_balas_enemigos.add(bala)
                self.tiempo_ultimo_ataque = ahora
        else:
            # Jefe monstruo: lanza solo un tipo de ataque a la vez (fuego, láser o espina)
            from ataques_jefe import BolaFuego, LaserJefe, EspinaJefe
            if ahora - self.tiempo_ultimo_disparo > 1200:
                ataque = random.choice(['fuego', 'laser', 'espina'])
                if ataque == 'fuego':
                    grupo_balas_enemigos.add(BolaFuego(self.rect.centerx, self.rect.bottom))
                elif ataque == 'laser':
                    grupo_balas_enemigos.add(LaserJefe(self.rect.centerx, self.rect.bottom))
                else:
                    grupo_balas_enemigos.add(EspinaJefe(self.rect.centerx, self.rect.bottom))
                self.tiempo_ultimo_disparo = ahora

    def update(self, width, *args, **kwargs):
        # Actualizar animación
        if self.frames:
            ahora = pygame.time.get_ticks()
            if ahora - self.tiempo_animacion > self.velocidad_animacion:
                # Guardar posición central
                center_x = self.rect.centerx
                center_y = self.rect.centery
                
                # Cambiar frame
                self.frame_actual = (self.frame_actual + 1) % len(self.frames)
                self.image = self.frames[self.frame_actual]
                
                # Actualizar rect y restaurar posición central
                self.rect = self.image.get_rect()
                self.rect.centerx = center_x
                self.rect.centery = center_y
                
                self.tiempo_animacion = ahora
        
        # Movimiento horizontal
        self.rect.x += self.velocidad_x * self.direccion
        if self.rect.right >= width:
            self.rect.right = width
            self.direccion *= -1
        if self.rect.left <= 0:
            self.rect.left = 0
            self.direccion *= -1

    def recibir_dano(self, cantidad):
        self.vida -= cantidad
        if self.vida <= 0:
            self.kill()
