import pygame

BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)


def texto_puntuacion(frame, text, size, x, y, align="center", color=BLANCO, bg=NEGRO, bold=True):
    font = pygame.font.SysFont('Arial', size, bold=bold)
    text_frame = font.render(text, True, color, bg)
    text_rect = text_frame.get_rect()
    if align == "center":
        text_rect.midtop = (x, y)
    else:
        text_rect.topleft = (x, y)
    frame.blit(text_frame, text_rect)


def barra_vida(frame, x, y, nivel, longitud=100):
    alto = 24
    fill_width = int((nivel / 100) * longitud)
    border = pygame.Rect(x, y, longitud, alto)
    fill_rect = pygame.Rect(x, y, fill_width, alto)
    # Color cian para vida
    pygame.draw.rect(frame, (0, 255, 255), fill_rect)
    pygame.draw.rect(frame, NEGRO, border, 4)


def cargar_explosiones():
    explosion_list = []
    for i in range(1, 13):
        explosion = pygame.image.load(f'explosion/{i}.png')
        explosion_list.append(explosion)
    return explosion_list

