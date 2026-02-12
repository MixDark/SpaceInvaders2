import pygame
import random
from jugador import Jugador
from enemigos import Enemigos
from jefe import Jefe
from balas import Balas, BalasEnemigos
from explosion import Explosion
from utils import texto_puntuacion, barra_vida, cargar_explosiones, BLANCO, NEGRO
from pantalla_gameover import PantallaGameOver
from powerups import PowerUp

pygame.init()
pygame.mixer.init() # Inicializar con valores por defecto para mayor compatibilidad
import os
BASE_PATH = os.path.dirname(os.path.abspath(__file__))

width = 1024
height = 800
window = pygame.display.set_mode((width, height), pygame.RESIZABLE)

try:
    import ctypes
    hwnd = pygame.display.get_wm_info()['window']
    ctypes.windll.user32.ShowWindow(hwnd, 3)  # SW_MAXIMIZE
    # Esperar un poco para que la ventana se maximice y obtener el nuevo tamaño
    pygame.event.pump()
    width, height = window.get_size()
except Exception:
    pass

pygame.display.set_caption('Space Invaders 2')

# Sonidos
laser_sonido = pygame.mixer.Sound('sonidos/laser.wav')
explosion_sonido = pygame.mixer.Sound('sonidos/explosion.wav')
explosion_sonido.set_volume(0.2) # Volumen base bajo
golpe_sonido = pygame.mixer.Sound('sonidos/golpe.wav')

def cambiar_musica(nivel):
    # Diccionario de canciones por nivel
    # Diccionario con los nombres reales de los archivos para cada nivel
    musica_por_nivel = {
        1: '3.Invitation.mp3',
        2: '4.Departure_for_Space.mp3',
        3: '5.Sand_Storm.mp3',
        4: '6. Aqua_Illusion.mp3',
        5: '7. Lucky_Zone.mp3',
        6: '8.In_the_wind.mp3',
        7: '9. Underground.mp3',
        8: '10. Easter_Stone.mp3',
        9: '11. Fire_Scramble.mp3',
        10: '12.Sharp_Shoot.mp3',
        11: '13.Cosmo _Plant.mp3',
        12: '14.Accident_Road.mp3',
        13: '15.Boss_on_Parade_1_Zub.mp3',
        14: '16.Boss_on_Parade_2_Death.mp3',
        15: '17.Boss_on_Parade_3_Crystal_Core.mp3',
        16: '18.Boss_on_Parade_4_MK_II.mp3',
        17: '19.Boss_on_Parade_5_Covered_Core.mp3',
        18: '20.Dark_Force.mp3',
        19: '22.Mechanical_Base.mp3',
        20: '23.Final_Shot.mp3',
        21: '24.Unpleasant_Cell.mp3',
        22: '25.Last_Struggle.mp3',
        23: '26.King_of_Kings.mp3',
        24: '27.Good_Luck!.mp3',
        25: '28.Everlasting.mp3',
        26: '29.Try_to_Star.mp3',
        27: '30.Easter_Stone.mp3',
        28: '31.Return_to_the_Star.mp3',
        29: '32.A_Long_Time_Ago.mp3',
        30: '33.Athena.mp3',
        31: '34.Hades.mp3',
        32: '35.Prometheus.mp3',
    }
    archivo = musica_por_nivel.get(nivel, '3.Invitation.mp3')
    ruta_completa = os.path.normpath(os.path.join(BASE_PATH, 'sonidos', archivo))
    try:
        if os.path.exists(ruta_completa):
            pygame.mixer.music.stop()
            pygame.mixer.music.load(ruta_completa)
            pygame.mixer.music.play(-1, 0.0)
            pygame.mixer.music.set_volume(1.0)
        else:
            print(f"[ADVERTENCIA] Archivo de música no encontrado: {ruta_completa}")
    except Exception as e:
        print(f"[ERROR] No se pudo reproducir la música: {ruta_completa}\n{e}")

# Recursos
fondo_original = pygame.image.load('imagenes/fondo1.jpg')
fondo = pygame.transform.scale(fondo_original, (width, height))
explosion_list = cargar_explosiones()

fps = 60
clock = pygame.time.Clock()


niveles = 32
nivel_actual = 1
score = 0
vidas = 3

pantalla_gameover = PantallaGameOver(window, width, height)

def mostrar_creditos():
    global width, height, window
    # Usar fondo32 para los créditos
    try:
        fondo_final = pygame.image.load('imagenes/fondo32.jpg')
        fondo_final = pygame.transform.scale(fondo_final, (width, height))
    except:
        fondo_final = pygame.Surface((width, height))
        fondo_final.fill((0, 0, 20)) # Azul oscuro por si falla
    
    creditos_txt = [
        "Space invaders 2",
        "¡Victoria total!",
        "",
        "Historia",
        "En el amanecer del año 2026, la humanidad enfrentó",
        "su prueba definitiva. Tras años de silencio, el",
        "Imperio Silencioso lanzó un ataque devastador",
        "desde los confines de la nebulosa oscura.",
        "",
        "Como último piloto de la flota estelar, atravesaste",
        "30 sectores infestados de legiones alienígenas,",
        "luchando contra monstruosidades orgánicas y naves",
        "nodrizas del tamaño de lunas.",
        "",
        "Al derrotar al Soberano Robot Alíen, el núcleo",
        "central ha colapsado, liberando a la Tierra de",
        "un destino sombrío. La paz ha vuelto, y tu nombre",
        "será recordado entre las estrellas.",
        "",
        "Creador",
        "Esteban Garcia",
        "",
        "Redes y código",
        "YouTube: @mixdarkdev",
        "https://www.youtube.com/@mixdarkdev",
        "GitHub: MixDark",
        "https://github.com/MixDark/",
        "",
        "Enemigos enfrentados",
        "- Exploradores del vacío",
        "- Destructores clase omega",
        "- Escoltas reales del vacío",
        "",
        "Jefes derrotados",
        "- Nivel 11: Monstruo primordial",
        "- Nivel 21: Nave nodriza x-1",
        "- Nivel 31: Soberano robot alíen",
        "",
        "Créditos técnicos",
        "Lenguaje: Python | Motor: Pygame",
        "Música: Konami (Gradius Series)",
        "Inspiración sonora: Gradius III y IV (SNES)",
        "",
        "¡Gracias por jugar!",
        "",
        "Presiona cualquier tecla para continuar"
    ]
    
    # Cargar recursos base para las "capturas"
    try:
        img_jugador = pygame.image.load('imagenes/A1.png').convert_alpha()
        img_enemigo = pygame.image.load('imagenes/E1.png').convert_alpha()
        img_enemigo = pygame.transform.scale(img_enemigo, (30, 20))
        img_jugador = pygame.transform.scale(img_jugador, (35, 35))
        jefes_img = {
            11: pygame.transform.scale(pygame.image.load('imagenes/jefe1.png').convert_alpha(), (100, 70)),
            21: pygame.transform.scale(pygame.image.load('imagenes/jefe2.png').convert_alpha(), (100, 70)),
            31: pygame.transform.scale(pygame.image.load('imagenes/jefe3.png').convert_alpha(), (100, 70))
        }
    except: pass

    miniaturas_niveles = []
    
    # Generar capturas para cada nivel (1 al 31)
    for i in range(1, 32):
        try:
            # 1. Fondo base
            img_f = pygame.image.load(f'imagenes/fondo{i}.jpg')
            surf = pygame.transform.scale(img_f, (380, 285))
            
            # 2. Dibujar Jugador (siempre presente en la captura)
            surf.blit(img_jugador, (172, 240))
            
            # 3. Dibujar Enemigos o Jefe
            if i in [11, 21, 31]:
                # Captura de Jefe (Centrado)
                surf.blit(jefes_img[i], (140, 50))
            else:
                # Formación de enemigos (Disposición orgánica/aleatoria como en la imagen)
                for _ in range(25): # Aproximadamente 25 enemigos visibles
                    x_e = random.randint(20, 330)
                    y_e = random.randint(15, 120)
                    surf.blit(img_enemigo, (x_e, y_e))
            
            miniaturas_niveles.append((f'Nivel {i}', surf))
        except:
            pass
    
    y_scroll = height
    clock = pygame.time.Clock()
    corriendo = True
    indice_miniatura = 0
    tiempo_cambio = pygame.time.get_ticks()
    
    # Asegurar que la música de victoria (Prometheus) suene AQUÍ (al inicio de créditos)
    cambiar_musica(32)

    while corriendo:
        clock.tick(60)
        window.blit(fondo_final, (0, 0))
        ahora = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                corriendo = False
        
        # Lógica del carrusel de miniaturas
        if ahora - tiempo_cambio > 2000: # Cambiar cada 2 segundos para dar tiempo a ver personajes
            indice_miniatura = (indice_miniatura + 1) % len(miniaturas_niveles)
            tiempo_cambio = ahora
            
        # Dibujar miniatura actual en la esquina superior derecha
        if miniaturas_niveles:
            nombre_m, m_img = miniaturas_niveles[indice_miniatura]
            x_mini = width - 400
            y_mini = 45
            w_mini, h_mini = 380, 285
            window.blit(m_img, (x_mini, y_mini))
            pygame.draw.rect(window, (255, 255, 255), (x_mini, y_mini, w_mini, h_mini), 3) 
            texto_puntuacion(window, nombre_m, 28, x_mini + w_mini // 2, y_mini + h_mini + 10, bg=None)

        offset = 0
        for linea in creditos_txt:
            # Dibujar con fondo None para transparencia
            texto_puntuacion(window, linea, 35, width // 2, y_scroll + offset, bg=None)
            offset += 50
        
        y_scroll -= 1  # Velocidad de scroll
        
        if y_scroll + offset < -50:
            corriendo = False
            
        pygame.display.flip()



def iniciar_juego():
    global score, vidas, nivel_actual, width, height, fondo, window
    score = 0
    vidas = 3
    nivel_actual = 1
    victoria = False
    cambiar_musica(nivel_actual) # Iniciar música del nivel 1
    run = True
    pausado = False
    grupo_jugador = pygame.sprite.Group()
    grupo_enemigos = pygame.sprite.Group()
    grupo_balas_jugador = pygame.sprite.Group()
    grupo_balas_enemigos = pygame.sprite.Group()
    grupo_powerups = pygame.sprite.Group()
    esperando_nivel = False
    tiempo_nivel_completado = 0
    esperando_oleada = False
    tiempo_oleada_completada = 0
    grupo_explosiones = pygame.sprite.Group()
    
    # Sistema de OLEADAS
    enemigos_por_oleada = 30
    enemigos_totales_nivel = 0
    enemigos_generados_nivel = 0
    bombas_disponibles = 5
    # Bandera de inicio eliminada por solicitud
    tiempo_inicio_nivel = pygame.time.get_ticks()
    musica_victoria_reproducida = False # Asegurar que Prometheus suene una vez

    player = Jugador(width, height)
    grupo_jugador.add(player)

    def crear_oleada():
        nonlocal enemigos_generados_nivel, enemigos_totales_nivel
        if nivel_actual in [11, 21, 31]:
            # NIVELES DE JEFE: Solo generamos 1 si no se ha generado
            if enemigos_generados_nivel == 0:
                from jefe import Jefe
                tipo = 1 if nivel_actual == 11 else (2 if nivel_actual == 21 else 3)
                jefe = Jefe(width, tipo=tipo)
                grupo_enemigos.add(jefe)
                enemigos_generados_nivel = 1
                enemigos_totales_nivel = 1
            return

        # Limitamos la cantidad a spawnear para que sea una oleada
        cantidad = min(enemigos_por_oleada, enemigos_totales_nivel - enemigos_generados_nivel)
        
        # Crear enemigos con mejor distribución
        posiciones_ocupadas = []
        intentos_max = 50  # Máximo de intentos para encontrar posición libre
        
        for i in range(cantidad):
            enemigo = Enemigos(width, nivel_actual)
            
            # Intentar encontrar una posición que no se superponga
            colocado = False
            for intento in range(intentos_max):
                # Posición aleatoria en la parte superior
                nueva_x = random.randrange(50, width - 50)
                nueva_y = random.randrange(50, int(height * 0.35))
                
                # Verificar si está muy cerca de otra posición ocupada
                muy_cerca = False
                for pos_x, pos_y in posiciones_ocupadas:
                    distancia = ((nueva_x - pos_x)**2 + (nueva_y - pos_y)**2)**0.5
                    if distancia < 60:  # Mínimo 60 píxeles de separación
                        muy_cerca = True
                        break
                
                if not muy_cerca:
                    enemigo.rect.x = nueva_x
                    enemigo.rect.y = nueva_y
                    posiciones_ocupadas.append((nueva_x, nueva_y))
                    colocado = True
                    break
            
            # Si no se pudo colocar después de muchos intentos, usar posición aleatoria
            if not colocado:
                enemigo.rect.y = random.randrange(50, int(height * 0.35))
            
            grupo_enemigos.add(enemigo)
        enemigos_generados_nivel += cantidad

    def lanzar_bomba():
        global score, nivel_actual, fondo, width, height
        nonlocal enemigos_totales_nivel, enemigos_generados_nivel, victoria, run, bombas_disponibles
        from explosion_centrada import ExplosionCentrada
        
        enemigos_lista = grupo_enemigos.sprites()
        if not enemigos_lista: return
        # Seleccionar hasta 5 enemigos al azar
        objetivos = random.sample(enemigos_lista, min(len(enemigos_lista), 5))
        for enemigo in objetivos:
            if isinstance(enemigo, Jefe):
                # Solo aplicar daño si no ha sido destruido
                if not hasattr(enemigo, 'destruido') or not enemigo.destruido:
                    enemigo.vida -= 200 # Gran daño al jefe (20% del tipo 1)
                    
                    # Crear explosión CENTRADA sobre el jefe
                    pos_centro = enemigo.rect.center
                    explo_impacto = ExplosionCentrada(pos_centro, explosion_list, tamano=(120, 120))
                    grupo_jugador.add(explo_impacto)
                    grupo_explosiones.add(explo_impacto)
                    explosion_sonido.play()
                    
                    if enemigo.vida <= 0:
                        enemigo.destruido = True
                        score += 1000
                        pos_explo = enemigo.rect.center
                        
                        # Crear explosión grande
                        explo = Explosion(pos_explo, explosion_list)
                        explo.image = pygame.transform.scale(explo.image, (160, 160))
                        grupo_jugador.add(explo)
                        explosion_sonido.set_volume(0.4) # Volumen de jefe (un poco más alto que base)
                        explosion_sonido.play()
                        
                        # Eliminar jefe del grupo para vaciar el grupo y activar el paso de nivel
                        enemigo.kill()
                        
                        # VICTORIA PREVENTIVA: Si es el boss final, aseguramos la victoria AQUÍ
                        if nivel_actual == 31:
                            victoria = True
                            
                        # LIMPIEZA TOTAL: Eliminar todos los enemigos y balas restantes para evitar muertes post-victoria
                        grupo_enemigos.empty()
                        grupo_balas_enemigos.empty()
            else:
                # Enemigo normal
                # Crear explosión CENTRADA sobre enemigos normales y defensores
                from explosion_centrada import ExplosionCentrada
                pos_centro = enemigo.rect.center
                explo = ExplosionCentrada(pos_centro, explosion_list, tamano=(70, 70))
                grupo_jugador.add(explo)
                grupo_explosiones.add(explo)
                explosion_sonido.play()
                score += 10
                enemigo.kill()


    # Inicializar el primer nivel
    if nivel_actual in [11, 21, 31]:
        enemigos_totales_nivel = 1
    else:
        enemigos_totales_nivel = 90 + (nivel_actual - 1) * 30
    enemigos_generados_nivel = 0
    bombas_disponibles = 5
    # Limpiar grupos
    grupo_enemigos.empty()
    grupo_balas_enemigos.empty()
    grupo_balas_jugador.empty()
    grupo_powerups.empty()
    crear_oleada()
    tiempo_inicio_nivel = pygame.time.get_ticks()
    bloqueo_subida_nivel = True

    while run:
        clock.tick(fps)
        window.blit(fondo, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.VIDEORESIZE:
                width, height = event.size
                window = pygame.display.set_mode((width, height), pygame.RESIZABLE)
                # Recargar y escalar el fondo actual
                fondo_original = pygame.image.load(f'imagenes/fondo{nivel_actual}.jpg' if nivel_actual > 1 else 'imagenes/fondo1.jpg')
                fondo = pygame.transform.scale(fondo_original, (width, height))
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pausado = not pausado
                # Selección manual de ARMAS (Teclas superiores y Numpad)
                elif event.key == pygame.K_1 or event.key == pygame.K_KP1:
                    player.poderes_activos['simple'] = pygame.time.get_ticks() + 3600000 
                    player.arma_preferida = 'simple'
                elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                    player.poderes_activos['doble'] = pygame.time.get_ticks() + 3600000
                    player.arma_preferida = 'doble'
                elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
                    player.poderes_activos['triple'] = pygame.time.get_ticks() + 3600000
                    player.arma_preferida = 'triple'
                elif event.key == pygame.K_4 or event.key == pygame.K_KP4:
                    player.poderes_activos['quintuple'] = pygame.time.get_ticks() + 3600000
                    player.arma_preferida = 'quintuple'
                elif event.key == pygame.K_5 or event.key == pygame.K_KP5:
                    player.poderes_activos['laser'] = pygame.time.get_ticks() + 3600000
                    player.arma_preferida = 'laser'
                elif event.key == pygame.K_6 or event.key == pygame.K_KP6:
                    if bombas_disponibles > 0:
                        lanzar_bomba()
                        bombas_disponibles -= 1
                elif event.key == pygame.K_7 or event.key == pygame.K_KP7:
                    player.poderes_activos['teledirigido'] = pygame.time.get_ticks() + 3600000
                    player.arma_preferida = 'teledirigido'
                elif event.key == pygame.K_8 or event.key == pygame.K_KP8:
                    player.poderes_activos['ripple'] = pygame.time.get_ticks() + 3600000
                    player.arma_preferida = 'ripple'
                elif event.key == pygame.K_9 or event.key == pygame.K_KP9:
                    player.poderes_activos['mega'] = pygame.time.get_ticks() + 3600000
                    player.arma_preferida = 'mega'
                pass # Eliminamos el disparo por evento único

        if pausado:
            texto_puntuacion(window, 'Pausa', 80, width // 2, height // 2 - 50)
            texto_puntuacion(window, 'Presiona P para continuar', 30, width // 2, height // 2 + 50)
            pygame.display.flip()
            continue

        # Disparo continuo si se mantiene presionada la tecla espacio
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_SPACE]:
            player.disparar(grupo_jugador, grupo_balas_jugador, laser_sonido, grupo_enemigos)

        grupo_jugador.update(width, height)
        grupo_enemigos.update(width, height)
        grupo_balas_jugador.update()
        grupo_balas_enemigos.update()
        grupo_powerups.update()
        grupo_explosiones.update()

        # Dibujar jugador con parpadeo de invulnerabilidad
        if not (player.invulnerable and (pygame.time.get_ticks() // 100) % 2 == 0):
            grupo_jugador.draw(window)
        
        player.dibujar_escudo(window)
        grupo_enemigos.draw(window)
        grupo_balas_jugador.draw(window)
        grupo_balas_enemigos.draw(window)
        grupo_powerups.draw(window)
        grupo_explosiones.draw(window)

        # Disparo y Habilidades del Jefe y Defensores
        from defensor import Defensor
        for e in grupo_enemigos:
            if isinstance(e, Jefe):
                if e.vida > 0:
                    e.disparar(grupo_jugador, grupo_balas_enemigos, laser_sonido)
                    e.spawn_escoltas(grupo_enemigos, width, nivel_actual)
                    # Dibujar barra de vida del jefe solo si está vivo
                    barra_width = 400
                    barra_x = (width // 2) - (barra_width // 2)
                    pygame.draw.rect(window, (50, 0, 0), (barra_x - 2, 98, barra_width + 4, 24))
                    barra_vida(window, barra_x, 100, int((e.vida / e.vida_max) * 100), barra_width)
                    # Mostrar nombre de jefe según el nivel
                    if nivel_actual == 11:
                        nombre_jefe = 'Jefe monstruo'
                    elif nivel_actual == 21:
                        nombre_jefe = 'Jefe nave nodriza'
                    elif nivel_actual == 31:
                        nombre_jefe = 'Jefe robot alienígena'
                    else:
                        nombre_jefe = 'Jefe'
                    texto_puntuacion(window, nombre_jefe, 25, width // 2, 135)
            elif isinstance(e, Defensor):
                # Los defensores también disparan
                e.disparar(grupo_balas_enemigos)

        # Colisión balas_jugador - enemigo
        # Las balas deben DESAPARECER al impactar (no seguir de largo)
        # El láser es la única excepción si queremos que atraviese, pero el usuario pidió que "den a la nave"
        # Así que haremos que todas las balas se consuman al impactar para mejor feedback
        colicion1 = pygame.sprite.groupcollide(grupo_enemigos, grupo_balas_jugador, False, True)
        
        for enemigo, balas_que_impactaron in colicion1.items():
            # Si es el jefe y ya fue destruido, ignorar
            if isinstance(enemigo, Jefe):
                if hasattr(enemigo, 'destruido') and enemigo.destruido:
                    continue
            
            for bala in balas_que_impactaron:
                # Cada bala individual aplica su daño
                poder_bala = 1
                if 'misil' in player.poderes_activos:
                    poder_bala = 5 # Los misiles son potentes
                
                enemigo.vida -= poder_bala
                
                # Crear explosión de impacto CENTRADA para feedback visual
                from explosion_centrada import ExplosionCentrada
                if isinstance(enemigo, Jefe):
                    # Explosión más grande para el jefe
                    explo_impacto = ExplosionCentrada(enemigo.rect.center, explosion_list, tamano=(80, 80))
                else:
                    explo_impacto = ExplosionCentrada(enemigo.rect.center, explosion_list, tamano=(50, 50))
                grupo_jugador.add(explo_impacto)
                grupo_explosiones.add(explo_impacto)
                explosion_sonido.play()

            if enemigo.vida <= 0:
                if isinstance(enemigo, Jefe):
                    # Verificar si ya fue destruido para evitar doble procesamiento
                    if hasattr(enemigo, 'destruido') and enemigo.destruido:
                        continue
                    
                    enemigo.destruido = True  # Marcar como destruido ANTES de todo
                    enemigo.destruido = True  # Marcar como destruido ANTES de todo
                    score += 1000
                    pos_explo = enemigo.rect.center
                    
                    # Crear explosión grande CENTRADA
                    from explosion_centrada import ExplosionCentrada
                    explo = ExplosionCentrada(pos_explo, explosion_list, tamano=(180, 180))
                    grupo_jugador.add(explo)
                    grupo_explosiones.add(explo)
                    explosion_sonido.set_volume(0.4)
                    explosion_sonido.play()
                    
                    # Eliminar jefe del grupo para vaciar el grupo y activar el paso de nivel
                    enemigo.kill()
                    
                    # VICTORIA PREVENTIVA: Si es el boss final, aseguramos la victoria AQUÍ
                    if nivel_actual == 31:
                        victoria = True
                        
                    # LIMPIEZA TOTAL: Eliminar todos los enemigos y balas restantes para evitar muertes post-victoria
                    grupo_enemigos.empty()
                    grupo_balas_enemigos.empty()
                    # El paso de nivel se gestionara automáticamente en el bucle principal.
                else:
                    # Enemigo normal o defensor - Explosión CENTRADA
                    from explosion_centrada import ExplosionCentrada
                    tamano_explo = (80, 80) if isinstance(enemigo, Defensor) else (60, 60)
                    explo = ExplosionCentrada(enemigo.rect.center, explosion_list, tamano=tamano_explo)
                    grupo_jugador.add(explo)
                    grupo_explosiones.add(explo)
                    explosion_sonido.set_volume(0.15)
                    explosion_sonido.play()
                    
                    # Puntos según el tipo de enemigo
                    if isinstance(enemigo, Defensor):
                        # Los defensores dan más puntos según su tipo
                        if enemigo.tipo_jefe == 1:
                            score += 15  # Pequeños monstruos
                        elif enemigo.tipo_jefe == 2:
                            score += 20  # Pequeñas naves nodrizas
                        else:
                            score += 25  # Pequeños robots
                    else:
                        score += 10  # Enemigos normales
                    
                    if random.random() < 0.10:
                        pwp = PowerUp(enemigo.rect.centerx, enemigo.rect.centery)
                        grupo_powerups.add(pwp)
                    
                    # Solo los enemigos normales disparan al morir
                    if not isinstance(enemigo, Defensor):
                        enemigo.disparar_enemigos(grupo_jugador, grupo_balas_enemigos, laser_sonido)
                    
                    enemigo.kill()
            
        # VENTAJA: Colisión balas_jugador - balas_enemigo
        # Las balas del jugador destruyen las balas enemigas
        pygame.sprite.groupcollide(grupo_balas_jugador, grupo_balas_enemigos, True, True)

        # Colisión jugador - balas_enemigo
        colicion2 = pygame.sprite.spritecollide(player, grupo_balas_enemigos, True)
        if player.tiene_escudo:
            colicion2 = [] # Ignorar daño si hay escudo
            
        # Colisión jugador - PowerUps
        pwp_hits = pygame.sprite.spritecollide(player, grupo_powerups, True)
        for pwp in pwp_hits:
            ahora_p = pygame.time.get_ticks()
            if pwp.tipo == 'vida':
                player.vida = min(100, player.vida + 25)
            elif pwp.tipo == 'misil':
                fin_actual = player.poderes_activos.get('misil', ahora_p)
                player.poderes_activos['misil'] = fin_actual + 15000 
                player.arma_preferida = 'misil'
            elif pwp.tipo == 'escudo':
                fin_actual = player.poderes_activos.get('escudo', ahora_p)
                player.poderes_activos['escudo'] = fin_actual + 10000 
            elif pwp.tipo == 'bomba':
                lanzar_bomba()
        # Protección durante la transición de nivel/victoria
        if run and not player.invulnerable and not esperando_nivel:
            for bala in colicion2:
                player.vida -= 5
                if player.vida <= 0:
                    if vidas > 0:
                        vidas -= 1
                        player.vida = 100
                        player.invulnerable = True
                        player.tiempo_invulnerable = pygame.time.get_ticks() + 2000
                        # Salir del bucle de balas si perdemos una vida para aprovechar la invulnerabilidad
                        break
                    else: # Solo Game Over si ya no quedaban vidas antes del impacto
                        # MERCY MODE: En niveles de jefe, NO PERMITIR GAME OVER
                        if nivel_actual in [11, 21, 31]:
                            vidas = 1
                            player.vida = 100
                            player.invulnerable = True
                            player.tiempo_invulnerable = pygame.time.get_ticks() + 2000
                            break
                        else:
                            vidas = 0
                            run = False
                            break
                explo1 = Explosion(bala.rect.center, explosion_list)
                grupo_jugador.add(explo1)
                golpe_sonido.play()
        
        if not run:
            # Salir de la función si ya no hay vidas
            pass 

        # Colisión jugador - enemigo
        if run:
            # Usamos False para que el enemigo no muera solo por tocar el escudo
            # Solo muere (True) si el jugador NO tiene escudo
            hits = pygame.sprite.spritecollide(player, grupo_enemigos, not player.tiene_escudo)
            
            if not player.tiene_escudo and not player.invulnerable and not esperando_nivel:
                from defensor import Defensor # Asegurar importación
                for hit in hits:
                    damage = 100 # Daño base (Jefe/Enemigo normal)
                    if isinstance(hit, Defensor):
                        damage = 20 # Los defensores hacen menos daño por contacto
                    
                    player.vida -= damage
                    if player.vida <= 0:
                        if vidas > 0:
                            vidas -= 1
                            player.vida = 100
                            player.invulnerable = True
                            player.tiempo_invulnerable = pygame.time.get_ticks() + 2000
                            # Salir del bucle de colisiones para aprovechar la invulnerabilidad
                            break
                        else: # Solo Game Over si ya no quedaban vidas antes del impacto
                             # MERCY MODE: En niveles de jefe, NO PERMITIR GAME OVER
                            if nivel_actual in [11, 21, 31]:
                                vidas = 1
                                player.vida = 100
                                player.invulnerable = True
                                player.tiempo_invulnerable = pygame.time.get_ticks() + 2000
                                break
                            else:
                                vidas = 0
                                run = False
                                break
            else:
                # Si tiene escudo, los enemigos simplemente rebotan o pasan
                pass
        
        if not run:
            # Forzar salida del bucle principal antes de dibujar los indicadores
            break


        # Indicador y Score - HUD DE DOS FILAS
        # FILA 1: Información básica
        texto_puntuacion(window, f'Vidas: {vidas}', 30, 20, 10, align="left")
        texto_puntuacion(window, f'Nivel: {nivel_actual}', 30, 180, 10, align="left")
        barra_vida(window, width - 425, 15, player.vida, 150)
        texto_puntuacion(window, f'Puntos: {score}', 30, width - 250, 10, align="left")

        # FILA 2: Arma, Bombas y Cronómetros
        arma_txt = player.arma_preferida.capitalize()
        texto_puntuacion(window, f'Arma: {arma_txt}', 28, 20, 50, align="left")
        texto_puntuacion(window, f'Bombas: {bombas_disponibles}', 28, 280, 50, align="left")
        
        # Cronómetros de poderes (con salto de línea si no caben)
        ahora_h = pygame.time.get_ticks()
        x_pwp = 500
        y_pwp = 52
        for poder, fin in list(player.poderes_activos.items()):
            if poder == 'simple': continue
            segundos = max(0, (fin - ahora_h) // 1000)
            if segundos < 3500: 
                # Si el próximo texto no cabe en el ancho de la ventana, saltar a la fila de abajo
                if x_pwp > width - 250:
                    x_pwp = 20
                    y_pwp += 40
                
                # Restaurar el fondo negro para mejor contraste
                texto_puntuacion(window, f'{poder.upper()}: {segundos}s', 24, x_pwp, y_pwp, align="left", bg=NEGRO)
                x_pwp += 280 # Espacio generoso para evitar que los textos largos se toquen

        # Lógica de OLEADAS y niveles
        if len(grupo_enemigos) == 0 and not esperando_nivel and not esperando_oleada:
            if enemigos_generados_nivel < enemigos_totales_nivel:
                # Si faltan enemigos por salir en este nivel, activamos espera para la siguiente oleada
                esperando_oleada = True
                tiempo_oleada_completada = pygame.time.get_ticks()
            else:
                # Si ya salieron todos, activamos el paso de nivel
                esperando_nivel = True
                tiempo_nivel_completado = pygame.time.get_ticks()
            
        if esperando_oleada:
            # Mostrar que viene una nueva oleada (Solo si no es el nivel del jefe)
            if nivel_actual != 11:
                texto_puntuacion(window, '¡Oleada destruida!', 50, width // 2, height // 2 - 20)
                texto_puntuacion(window, 'Preparando siguientes enemigos...', 30, width // 2, height // 2 + 30)
            # Aumentamos el retraso a 2.5 segundos para que sea evidente que terminó
            if pygame.time.get_ticks() - tiempo_oleada_completada > 2500:
                crear_oleada()
                esperando_oleada = False

        if esperando_nivel:
            if nivel_actual in [11, 21, 31]:
                # Música y mensaje especial por derrotar a un jefe (Solo si no es victoria final)
                if nivel_actual != 31 and not musica_victoria_reproducida:
                    try:
                        prom_path = os.path.normpath(os.path.join(BASE_PATH, 'sonidos/35.Prometheus.mp3'))
                        if os.path.exists(prom_path):
                            pygame.mixer.music.stop()
                            pygame.mixer.music.load(prom_path)
                            pygame.mixer.music.play()
                            musica_victoria_reproducida = True
                    except: pass
                
                texto_puntuacion(window, '¡MISIÓN CUMPLIDA!', 70, width // 2, height // 2 - 30)
                if nivel_actual == 31:
                    texto_puntuacion(window, 'Has superado todos los niveles', 40, width // 2, height // 2 + 50)
            else:
                # Mostrar mensaje de nivel completado normal
                texto_puntuacion(window, f'Nivel {nivel_actual} completado', 50, width // 2, height // 2)
                texto_puntuacion(window, 'Preparando siguiente oleada...', 30, width // 2, height // 2 + 60)
            
            # Esperar antes de pasar al siguiente (más tiempo si es el jefe)
            espera = 6000 if nivel_actual in [11, 21, 31] else 2000
            if pygame.time.get_ticks() - tiempo_nivel_completado > espera:
                if nivel_actual == 31:
                    victoria = True
                    run = False
                else:
                    nivel_actual += 1
                    bombas_disponibles = 5
                    cambiar_musica(nivel_actual) # Cambiar música al nuevo nivel
                    esperando_nivel = False
                    musica_victoria_reproducida = False # Resetear para el próximo jefe
                    tiempo_inicio_nivel = pygame.time.get_ticks()
                    # Cargar el fondo del nuevo nivel
                    nombre_fondo = f'imagenes/fondo{nivel_actual}.jpg'
                    try:
                        fondo_original = pygame.image.load(nombre_fondo)
                    except pygame.error:
                        fondo_original = pygame.image.load('imagenes/fondo1.jpg')
                    fondo = pygame.transform.scale(fondo_original, (width, height))
                    
                    # Limpiar pantalla para el nuevo nivel
                    grupo_enemigos.empty()
                    grupo_balas_enemigos.empty()
                    grupo_balas_jugador.empty()
                    grupo_powerups.empty()

                    # Preparar las oleadas del nuevo nivel
                    if nivel_actual in [11, 21, 31]:
                        enemigos_totales_nivel = 1
                    else:
                        enemigos_totales_nivel = 90 + (nivel_actual - 1) * 30
                    enemigos_generados_nivel = 0
                    crear_oleada()
        pygame.display.flip()

    if victoria:
        mostrar_creditos()

    pantalla_gameover.mostrar(score, width, height, victoria)
    return pantalla_gameover.esperar_reinicio()


if __name__ == '__main__':
    while True:
        reiniciar = iniciar_juego()
        if not reiniciar:
            break
    pygame.quit()
