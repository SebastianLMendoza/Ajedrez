"""
Responsable de registrar la actividad del usuario.
"""

import pygame as p
import MotorAjedrez
import AjedrezIA

ANCHO = ALTO = 512
DIMENSION = 8
SQ_SIZE = ALTO / DIMENSION
MAX_FPS = 15
IMAGES = {}

def cargarImagenes():
    piezas = ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR', 'bp',
              'wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR', 'wp'
              ]
    for pieza in piezas:
        IMAGES[pieza] = p.transform.scale(p.image.load("images/" + pieza + ".png"), (SQ_SIZE, SQ_SIZE))

def main():
    p.init()
    pantalla = p.display.set_mode((ANCHO, ALTO))
    p.display.set_caption('Ajedrez')
    Icon = p.image.load('logo.png')
    p.display.set_icon(Icon)
    reloj = p.time.Clock()
    pantalla.fill(p.Color("white"))
    gs = MotorAjedrez.EstadoJuego()
    valiMovis = gs.getMovValidos()
    moviHecho = False
    cargarImagenes()
    running = True
    sqSeleccionado = ()
    clicksJugador = []
    animar = False
    gameover = False
    jugadorUno = True
    jugadorDos = False

    while running:

        turnoHumano = (gs.moverParaBlanco and jugadorUno) or (not gs.moverParaBlanco and jugadorDos)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameover and turnoHumano:
                    localizacion = p.mouse.get_pos()
                    col = localizacion[0] // SQ_SIZE
                    row = localizacion[1] // SQ_SIZE
                    if sqSeleccionado == (row, col):
                        sqSeleccionado = ()
                        clicksJugador = []
                    else:
                        sqSeleccionado = (row, col)
                        clicksJugador.append(sqSeleccionado)

                    if len(clicksJugador) == 1:
                        if gs.tabla[int(clicksJugador[0][0])][int(clicksJugador[0][1])] == '--':
                            clicksJugador = []
                            sqSeleccionado = ()

                        elif gs.moverParaBlanco and gs.tabla[int(clicksJugador[0][0])][int(clicksJugador[0][1])][0] == 'b':
                            clicksJugador = []
                            sqSeleccionado = ()

                        elif not gs.moverParaBlanco and gs.tabla[int(clicksJugador[0][0])][int(clicksJugador[0][1])][
                            0] == 'w':
                            clicksJugador = []
                            sqSeleccionado = ()
                    elif len(clicksJugador) == 2:

                        if gs.tabla[int(clicksJugador[0][0])][int(clicksJugador[0][1])][0] == \
                                gs.tabla[int(clicksJugador[1][0])][int(clicksJugador[1][1])][0]:
                            clicksJugador.remove(clicksJugador[0])

                        else:

                            movi = MotorAjedrez.Movi(clicksJugador[0], clicksJugador[1], gs.tabla)
                            for i in range(len(valiMovis)):
                                if movi == valiMovis[i]:
                                    gs.realMov(valiMovis[i])
                                    moviHecho = True
                                    animar = True
                                    sqSeleccionado = ()
                                    clicksJugador = []
                            if not moviHecho:
                                clicksJugador = [clicksJugador[0]]

            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    if jugadorDos:
                        gs.deshacerMov()

                    else:
                        gs.deshacerMov()
                        gs.deshacerMov()

                    moviHecho = True
                    animar = False
                    gameover = False

                if e.key == p.K_r:
                    gs = MotorAjedrez.EstadoJuego()
                    valiMovis = gs.getMovValidos()
                    sqSeleccionado = ()
                    clicksJugador = []
                    moviHecho = False
                    animar = False
                    gameover = False

        if not gameover and not turnoHumano and valiMovis != []:

            if len(gs.movRegis) >= 4:
                if gs.movRegis[-1].startSq == gs.movRegis[-3].endSq and \
                        gs.movRegis[-1].endSq == gs.movRegis[-3].startSq and \
                        gs.movRegis[-2].startSq == gs.movRegis[-4].endSq and \
                        gs.movRegis[-2].endSq == gs.movRegis[-4].startSq:
                    moviIA = AjedrezIA.getMovAleatorio(valiMovis)
                else:
                    moviIA = AjedrezIA.getNegaMaxAlphaBeta(gs, valiMovis)
                    if moviIA:
                        pass
                    else:
                        moviIA = AjedrezIA.getMovAleatorio(valiMovis)

                gs.realMov(moviIA)
                moviHecho = True
                animar = True

            else:
                moviIA = AjedrezIA.getNegaMaxAlphaBeta(gs, valiMovis)
                if moviIA:
                    pass
                else:
                    moviIA = AjedrezIA.getMovAleatorio(valiMovis)
                gs.realMov(moviIA)
                moviHecho = True
                animar = True

        else:
            pass

        if moviHecho:
            if animar:
                animarMovi(gs.movRegis[-1], pantalla, gs.tabla, reloj)
            valiMovis = gs.getMovValidos()
            moviHecho = False
            animar = False

        dibujarGameState(pantalla, gs, valiMovis, sqSeleccionado)

        if (gs.moverParaBlanco and gs.checkmate) or (gs.moverParaBlanco and len(valiMovis) == 0):
            getTexto(pantalla, 'Negro Gana')
            gameover = True
        elif (not gs.moverParaBlanco and gs.checkmate) or (not gs.moverParaBlanco and len(valiMovis) == 0):
            getTexto(pantalla, "Blanco Gana")
            gameover = True
        elif gs.stalemate:
            getTexto(pantalla, 'Empate')

        reloj.tick(MAX_FPS)
        p.display.flip()

def iluminarCuad(pantalla, gs, movisValid, sqSeleccionado):
    if sqSeleccionado != ():
        r, c = sqSeleccionado
        if gs.tabla[int(r)][int(c)][0] == ('w' if gs.moverParaBlanco else 'b'):
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)
            s.fill(p.Color('blue'))
            pantalla.blit(s, (c * SQ_SIZE, r * SQ_SIZE))
            s.fill(p.Color('yellow'))
            for movi in movisValid:
                if movi.startRow == r and movi.startCol == c:
                    pantalla.blit(s, (movi.endCol * SQ_SIZE, movi.endRow * SQ_SIZE))


def dibujarGameState(pantalla, gs, movisValid, sqSeleccionado):
    dibujarTabla(pantalla)
    iluminarCuad(pantalla, gs, movisValid, sqSeleccionado)
    dibujarPiezas(pantalla, gs.tabla)

def dibujarTabla(pantalla):
    global colores
    colores = [p.Color(234, 221, 202), p.Color(193, 154, 107)]

    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colores[((r + c) % 2)]
            p.draw.rect(pantalla, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def dibujarPiezas(pantalla, tabla):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            pieza = tabla[r][c]
            if pieza != '--':
                pantalla.blit(IMAGES[pieza], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def animarMovi(movi, pantalla, tabla, reloj):
    global colores
    coords = []
    dR = movi.endRow - movi.startRow
    dC = movi.endCol - movi.startCol
    framesPerCuad = 10
    frameCont = (abs(dR) + abs(dC)) * framesPerCuad
    for frame in range(frameCont + 1):
        r, c = (movi.startRow + dR * frame / frameCont, movi.startCol + dC * frame / frameCont)
        dibujarTabla(pantalla)
        dibujarPiezas(pantalla, tabla)

        color = colores[(movi.endRow + movi.endCol) % 2]
        endCuad = p.Rect(movi.endCol * SQ_SIZE, movi.endRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(pantalla, color, endCuad)

        if movi.piezCap != '--':
            if movi.enPassant:
                enPassantRow = movi.endRow + 1 if movi.piezCap[0] == 'b' else movi.endRow - 1
                endCuad = p.Rect(movi.endCol * SQ_SIZE, enPassantRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)

            pantalla.blit(IMAGES[movi.piezCap], endCuad)
        pantalla.blit(IMAGES[movi.piezMov], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        reloj.tick(60)


def getTexto(screen, texto):
    fuente = p.font.SysFont('Helvitca', 32, True, False)
    objetoTexto = fuente.render(texto, 0, p.Color('White'))
    localTexto = p.Rect(0, 0, ANCHO, ALTO).move(ANCHO / 2 - objetoTexto.get_width() / 2,
                                                  ALTO / 2 - objetoTexto.get_height() / 2)
    screen.blit(objetoTexto, localTexto)
    objetoTexto = fuente.render(texto, 0, p.Color('Black'))
    screen.blit(objetoTexto, localTexto.move(2, 2))


if __name__ == '__main__':
    main()