"""
Responsable de registrar la actividad del usuario.
"""

import pygame as p
from Ajedrez import MotorAjedrez

ANCHO = ALTO = 512
DIMENSION = 8
CU_TAM = ALTO // DIMENSION
MAX_FPS = 15
IMAGEN = {}

'''
Inicializa el directorio de imagenes.
'''
def cargarImag():
    piezas = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for pieza in piezas:
        IMAGEN[pieza] = p.transform.scale(p.image.load("images/" + pieza + ".png"), (CU_TAM, CU_TAM))

'''
Encargado de la actividad del usuario
'''

def main():
    p.init()
    screen = p.display.set_mode((ANCHO, ALTO))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = MotorAjedrez.EstadoJuego()
    validMov = gs.getMovValid()
    moviHecho = False
    cargarImag()
    running = True
    sqSelected = ()
    clickJugad = []
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0]//CU_TAM
                row = location[1]//CU_TAM
                if sqSelected == (row, col):
                    sqSelected = ()
                    clickJugad = []
                else:
                    sqSelected = (row, col)
                    clickJugad.append(sqSelected)
                if len(clickJugad) == 2:
                    movi = MotorAjedrez.Movi(clickJugad[0], clickJugad[1], gs.tabla)
                    print(movi.getAjedNot())
                    if movi in validMov:
                        gs.realMov(movi)
                        moviHecho = True
                        sqSelected = ()
                        clickJugad = []
                    else:
                        clickJugad = [sqSelected]
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.desMov()
                    moviHecho = True
        if moviHecho:
            validMov = gs.getMovValid()
            moviHecho = False
        dibEstadoJuego(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

def dibEstadoJuego(screen, gs):
    dibTabla(screen)
    dibPiezas(screen, gs.tabla)

def dibTabla(screen):
    colors = [p.Color("white"), p.Color("grey")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c)%2)]
            p.draw.rect(screen, color, p.Rect(c*CU_TAM, r*CU_TAM, CU_TAM, CU_TAM))

def dibPiezas(screen, tabla):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            pieza = tabla[r][c]
            if pieza != "--":
                screen.blit(IMAGEN[pieza], p.Rect(c*CU_TAM, r*CU_TAM, CU_TAM, CU_TAM))



if __name__ == "__main__":
    main()