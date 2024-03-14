"""
La IA del juego. No hay mucho que explicar. :P
"""

import random

piezaPuntos = {'K': 0, 'Q': 10, 'R': 5, 'B': 3, 'N': 3, 'p': 1}
CHECKMATE = 1000
STALEMATE = 0
PROFUNDIDAD = 3

caballoPuntos = [[1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 2, 2, 2, 2, 2, 2, 1],
                 [1, 2, 3, 3, 3, 3, 2, 1],
                 [1, 2, 3, 4, 4, 3, 2, 1],
                 [1, 2, 3, 4, 4, 3, 2, 1],
                 [1, 2, 3, 3, 3, 3, 2, 1],
                 [1, 2, 2, 2, 2, 2, 2, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1]]

alfilPuntos = [[4, 3, 2, 1, 1, 2, 3, 4],
               [3, 4, 3, 2, 2, 3, 4, 3],
               [2, 3, 4, 3, 3, 4, 3, 2],
               [1, 2, 3, 4, 4, 3, 2, 1],
               [1, 2, 3, 4, 4, 3, 2, 1],
               [2, 3, 4, 3, 3, 4, 3, 2],
               [3, 4, 3, 2, 2, 3, 4, 3],
               [4, 3, 2, 1, 1, 2, 3, 4]]

reinaPuntos = [[1, 1, 1, 3, 1, 1, 1, 1],
               [1, 2, 3, 3, 3, 1, 1, 1],
               [1, 4, 3, 3, 3, 4, 2, 1],
               [1, 2, 3, 3, 3, 2, 2, 1],
               [1, 2, 3, 3, 3, 2, 2, 1],
               [1, 4, 3, 3, 3, 4, 2, 1],
               [1, 1, 2, 3, 3, 1, 1, 1],
               [1, 1, 1, 3, 1, 1, 1, 1]]

torrePuntos = [[4, 3, 4, 4, 4, 4, 3, 4],
               [4, 4, 4, 4, 4, 4, 4, 4],
               [1, 1, 2, 3, 3, 2, 1, 1],
               [1, 2, 3, 4, 4, 3, 2, 1],
               [1, 2, 3, 4, 4, 3, 2, 1],
               [1, 1, 2, 2, 2, 2, 1, 1],
               [4, 4, 4, 4, 4, 4, 4, 4],
               [4, 3, 4, 4, 4, 4, 3, 4]]

peonBlancoPuntos = [[8, 8, 8, 8, 8, 8, 8, 8],
                    [8, 8, 8, 8, 8, 8, 8, 8],
                    [5, 6, 6, 7, 7, 6, 6, 5],
                    [2, 3, 3, 5, 5, 3, 3, 2],
                    [1, 2, 3, 4, 4, 3, 2, 1],
                    [1, 1, 2, 3, 3, 2, 1, 1],
                    [1, 1, 1, 0, 0, 1, 1, 1],
                    [0, 0, 0, 0, 0, 0, 0, 0]]

peonNegroPuntos = [[0, 0, 0, 0, 0, 0, 0, 0],
                   [1, 1, 1, 0, 0, 1, 1, 1],
                   [1, 1, 2, 3, 3, 2, 1, 1],
                   [1, 2, 3, 4, 4, 3, 2, 1],
                   [2, 3, 3, 5, 5, 3, 3, 2],
                   [5, 6, 6, 7, 7, 6, 6, 5],
                   [8, 8, 8, 8, 8, 8, 8, 8],
                   [8, 8, 8, 8, 8, 8, 8, 8]]

piezaPosicionPuntos = {'N': caballoPuntos,
                       'Q': reinaPuntos,
                       'B': alfilPuntos,
                       'R': torrePuntos,
                       'bp': peonNegroPuntos,
                       'wp': peonBlancoPuntos}


def getMovAleatorio(movivalido):
    return movivalido[random.randint(0, len(movivalido) - 1)]

def getMejorMovi(gs, moviValidos):
    getMultiplicador = 1 if gs.moverParaBlanco else -1
    OponenteMinMaxPuntos = CHECKMATE
    mejorJugada = None
    random.shuffle(moviValidos)
    for moviJugador in moviValidos:
        gs.realMov(moviJugador)
        moviOponente = gs.getMovValidos()
        if gs.stalemate:
            oponenteMaxPuntos = STALEMATE
        elif gs.checkmate:
            oponenteMaxPuntos = -CHECKMATE
        else:
            oponenteMaxPuntos = -CHECKMATE
            for oponentesMuev in moviOponente:
                gs.realMov(oponentesMuev)
                gs.getMovValidos()
                if gs.checkmate:
                    puntosTabla = CHECKMATE
                elif gs.stalemate:
                    puntosTabla = STALEMATE
                else:
                    puntosTabla = -getMultiplicador * puntosMat(gs.tabla)
                if puntosTabla > oponenteMaxPuntos:
                    oponenteMaxPuntos = puntosTabla
                    mejorJugada = moviJugador
                gs.deshacerMov()

        if oponenteMaxPuntos < OponenteMinMaxPuntos:
            OponenteMinMaxPuntos = oponenteMaxPuntos
            mejorJugada = moviJugador
        gs.deshacerMov()

    return mejorJugada


def puntosMat(tabla):
    tablaPuntos = 0
    for row in tabla:
        for cuadrado in row:
            if cuadrado[0] == 'w':
                tablaPuntos += piezaPuntos[cuadrado[1]]
            elif cuadrado[0] == 'b':
                tablaPuntos -= piezaPuntos[cuadrado[1]]

    return tablaPuntos

def getMejorMoviMinMax(gs, moviValido):
    global sigMovi
    sigMovi = None
    getMoviMinMax(gs, moviValido, PROFUNDIDAD, gs.moverParaBlanco)
    return sigMovi


def getMoviMinMax(gs, moviValidos, profundidad, moverParaBlanco):
    global sigMovi
    if profundidad == 0:
        return tablaPuntos(gs)

    if moverParaBlanco:
        maxPuntos = -CHECKMATE
        for movi in moviValidos:
            gs.realMov(movi)
            sigMovimiento = gs.getMovValidos()
            puntos = getMoviMinMax(gs, sigMovimiento, profundidad - 1, False)
            if puntos > maxPuntos:
                maxPuntos = puntos
                if profundidad == PROFUNDIDAD:
                    sigMovi = movi
            gs.deshacerMov()
        return maxPuntos

    else:
        minPuntos = CHECKMATE
        for movi in moviValidos:
            gs.realMov(movi)
            sigMovimiento = gs.getMovValidos()
            puntos = getMoviMinMax(gs, sigMovimiento, profundidad - 1, True)
            if puntos < minPuntos:
                minPuntos = puntos
                if profundidad == PROFUNDIDAD:
                    sigMovi = movi

            gs.deshacerMov()
        return minPuntos

def tablaPuntos(gs):
    if gs.checkmate:
        if gs.moverParaBlanco:
            return -CHECKMATE
        else:
            return CHECKMATE

    elif gs.stalemate:
        return STALEMATE

    puntoTabla = 0
    for row in range(len(gs.tabla)):
        for col in range(len(gs.tabla[row])):
            cuadrado = gs.tabla[row][col]
            if cuadrado != '--':
                piezaPosiPuntos = 0
                if cuadrado[1] != 'K':
                    if cuadrado[1] == 'p':
                        piezaPosiPuntos = piezaPosicionPuntos[cuadrado][row][col]
                    else:
                        piezaPosiPuntos = piezaPosicionPuntos[cuadrado[1]][row][col]

                if cuadrado[0] == 'w':
                    puntoTabla += piezaPuntos[cuadrado[1]] + piezaPosiPuntos * 0.1
                elif cuadrado[0] == 'b':
                    puntoTabla -= piezaPuntos[cuadrado[1]] + piezaPosiPuntos * 0.1

    return puntoTabla

def getMejorMoviNegaMax(gs, moviVali):
    global sigMovi

    sigMovi = None
    getMoviNegaMax(gs, moviVali, PROFUNDIDAD, 1 if gs.moverParaBlanco else -1)
    return sigMovi


def getMoviNegaMax(gs, validoMovis, profundidad, multiplicadorTurno):
    global sigMovi

    if profundidad == 0:
        return multiplicadorTurno * tablaPuntos(gs)

    puntosMaximos = -CHECKMATE
    random.shuffle(validoMovis)
    for movi in validoMovis:
        gs.realMov(movi)
        sigMovis = gs.getMovValidos()
        puntuacion = -getMoviNegaMax(gs, sigMovis, profundidad - 1, -multiplicadorTurno)
        if puntuacion > puntosMaximos:
            puntosMaximos = puntuacion
            if profundidad == PROFUNDIDAD:
                sigMovi = movi
        gs.deshacerMov()
    return puntosMaximos

def getNegaMaxAlphaBeta(gs, movisValidos):
    global sigMovi
    sigMovi = None
    getMoviNegaMaxAB(gs, movisValidos, PROFUNDIDAD, -CHECKMATE, CHECKMATE, 1 if gs.moverParaBlanco else -1)
    return sigMovi


def getMoviNegaMaxAB(gs, movValidos, profundidad, alpha, beta, multiTurno):
    global sigMovi

    if profundidad == 0:
        return multiTurno * tablaPuntos(gs)

    puntosMax = -CHECKMATE
    random.shuffle(movValidos)
    for move in movValidos:
        gs.realMov(move)
        sigMovis = gs.getMovValidos()
        puntuacion = -getMoviNegaMaxAB(gs, sigMovis, profundidad - 1, -beta, -alpha, -multiTurno)
        if puntuacion > puntosMax:
            puntosMax = puntuacion
            if profundidad == PROFUNDIDAD:
                sigMovi = move
        gs.deshacerMov()
        if puntosMax > alpha:
            alpha = puntosMax
        if alpha >= beta:
            break

    return puntosMax