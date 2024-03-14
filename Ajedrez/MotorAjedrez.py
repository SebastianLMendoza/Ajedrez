"""
Responsable de administrar el estado del juego, y de los movimientos validos.
"""

class EstadoJuego():
    def __init__(self) -> None:
        self.tabla = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']]

        self.moverParaBlanco = True
        self.movRegis = []
        self.movFuncion = {'p': self.getPeonMov, 'N': self.getCaballoMov,
                              'R': self.getTorreMov,
                              'B': self.getAlfilMoves, 'Q': self.getReinaMov, 'K': self.getReyMov}

        self.localReyBlanco = (7, 4)
        self.localReyNegro = (0, 4)

        self.enCheck = False
        self.pins = []
        self.checks = []

        self.enpassantPosible = ()
        self.enpassantPosibleRegis = [self.enpassantPosible]

        self.actualEnroqueDer = EnroqueDer(True, True, True, True)
        self.enroqueDerRegis = [EnroqueDer(self.actualEnroqueDer.wks, self.actualEnroqueDer.bks,
                                           self.actualEnroqueDer.wqs, self.actualEnroqueDer.bqs)]
        self.deshFlag = False
        self.checkmate = False
        self.stalemate = False

    def realMov(self, movi):
        self.tabla[movi.startRow][movi.startCol] = '--'
        self.tabla[movi.endRow][movi.endCol] = movi.piezMov
        self.movRegis.append(movi)
        self.moverParaBlanco = not self.moverParaBlanco

        if movi.piezMov == 'wK':
            self.localReyBlanco = (movi.endRow, movi.endCol)
        elif movi.piezMov == 'bK':
            self.localReyNegro = (movi.endRow, movi.endCol)

        if movi.esPeonPromocion:
            self.tabla[movi.endRow][movi.endCol] = movi.piezMov[0] + 'Q'

        if movi.enPassant:
            self.tabla[movi.startRow][movi.endCol] = '--'

        if movi.piezMov[1] == 'p' and abs(movi.startRow - movi.endRow) == 2:
            self.enpassantPosible = ((movi.startRow + movi.endRow) // 2, movi.startCol)
        else:
            self.enpassantPosible = ()

        if movi.esEnroqueMov:
            if movi.endCol - movi.startCol == 2:
                self.tabla[movi.endRow][movi.endCol - 1] = self.tabla[movi.endRow][movi.endCol + 1]
                self.tabla[movi.endRow][movi.endCol + 1] = '--'
            else:
                self.tabla[movi.endRow][movi.endCol + 1] = self.tabla[movi.endRow][movi.endCol - 2]
                self.tabla[movi.endRow][movi.endCol - 2] = '--'

        self.enpassantPosibleRegis.append(self.enpassantPosible)

        self.actEnroqueDere(movi)
        self.enroqueDerRegis.append(EnroqueDer(self.actualEnroqueDer.wks, self.actualEnroqueDer.bks,
                                               self.actualEnroqueDer.wqs, self.actualEnroqueDer.bqs))

    def deshacerMov(self):
        if len(self.movRegis) != 0:
            movi = self.movRegis.pop()
            self.tabla[movi.startRow][movi.startCol] = movi.piezMov
            self.tabla[movi.endRow][movi.endCol] = movi.piezCap
            self.moverParaBlanco = not self.moverParaBlanco

            if movi.piezMov == 'wK':
                self.localReyBlanco = (movi.startRow, movi.startCol)
            elif movi.piezMov == 'bK':
                self.localReyNegro = (movi.startRow, movi.startCol)

            if movi.enPassant:
                self.tabla[movi.endRow][movi.endCol] = '--'
                self.tabla[movi.startRow][
                    movi.endCol] = movi.piezCap

            self.enpassantPosibleRegis.pop()
            self.enpassantPosible = self.enpassantPosibleRegis[-1]

            self.enroqueDerRegis.pop()
            self.actualEnroqueDer = self.enroqueDerRegis[-1]

            if movi.esEnroqueMov:
                if movi.endCol - movi.startCol == 2:
                    self.tabla[movi.endRow][movi.endCol + 1] = self.tabla[movi.endRow][
                        movi.endCol - 1]
                    self.tabla[movi.endRow][movi.endCol - 1] = '--'

                else:
                    self.tabla[movi.endRow][movi.endCol - 2] = self.tabla[movi.endRow][movi.endCol + 1]
                    self.tabla[movi.endRow][movi.endCol + 1] = '--'

            self.checkmate = False
            self.stalemate = False

    def actEnroqueDere(self, movi):

        if movi.piezMov == 'wK':
            self.actualEnroqueDer.wks = False
            self.actualEnroqueDer.wqs = False

        elif movi.piezMov == 'bK':
            self.actualEnroqueDer.bks = False
            self.actualEnroqueDer.bqs = False

        elif movi.piezMov == 'wR':
            if movi.startRow == 7:
                if movi.startCol == 0:
                    self.actualEnroqueDer.wqs = False
                elif movi.startCol == 7:
                    self.actualEnroqueDer.wks = False

        elif movi.piezMov == 'bR':
            if movi.startRow == 0:
                if movi.startCol == 0:
                    self.actualEnroqueDer.wqs = False
                elif movi.startCol == 7:
                    self.actualEnroqueDer.wks = False

        if movi.piezCap == 'wR':
            if movi.endRow == 7:
                if movi.endCol == 0:
                    self.actualEnroqueDer.wqs = False
                elif movi.endCol == 7:
                    self.actualEnroqueDer.wks = False

        elif movi.piezCap == 'bR':
            if movi.endRow == 0:
                if movi.endCol == 0:
                    self.actualEnroqueDer.bqs = False
                elif movi.endCol == 7:
                    self.actualEnroqueDer.bks = False

    def getMovValidos(self):
        movis = []
        self.enCheck, self.pins, self.checks, aliado = self.verPinsYChecks()
        if self.moverParaBlanco:
            reyRow = self.localReyBlanco[0]
            reyCol = self.localReyBlanco[1]
        else:
            reyRow = self.localReyNegro[0]
            reyCol = self.localReyNegro[1]

        if self.enCheck:
            if len(self.checks) == 1:
                movis = self.getTodoMovis()

                check = self.checks[0]
                checkRow = check[0]
                checkCol = check[1]
                piezaChecking = self.tabla[checkRow][checkCol]
                if piezaChecking[1] == 'N':
                    cuadValidos = [(checkRow, checkCol)]
                else:
                    cuadValidos = []
                    for i in range(1, 8):
                        cuadValido = (reyRow + check[2] * i, reyCol + check[3] * i)
                        cuadValidos.append(cuadValido)
                        if cuadValido[0] == checkRow and cuadValido[
                            1] == checkCol:
                            break

                for i in range(len(movis) - 1, -1, -1):
                    if movis[i].piezMov[1] != 'K':
                        if not (movis[i].endRow, movis[i].endCol) in cuadValidos:
                            movis.remove(movis[i])

            else:
                self.getReyMov(reyRow, reyCol, movis)

        else:
            movis = self.getTodoMovis()

        if len(movis) == 0:
            if self.enCheck:
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False

        self.getEnroqueMov(reyRow, reyCol, movis, 'w' if self.moverParaBlanco else 'b')

        return movis

    def getTodoMovis(self):
        movis = []
        for r in range(len(self.tabla)):
            for c in range(len(self.tabla[r])):
                turno = self.tabla[r][c][0]
                if (turno == 'w' and self.moverParaBlanco) or (turno == 'b' and not self.moverParaBlanco):
                    piece = self.tabla[r][c][1]
                    self.movFuncion[piece](r, c, movis)

        return movis

    def verPinsYChecks(self):
        pins = []
        checks = []
        enCheck = False

        if self.moverParaBlanco:
            colorEnemigo = 'b'
            colorAliado = 'w'
            startRow = self.localReyBlanco[0]
            startCol = self.localReyBlanco[1]
        else:
            colorEnemigo = 'w'
            colorAliado = 'b'
            startRow = self.localReyNegro[0]
            startCol = self.localReyNegro[1]

        direcciones = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(direcciones)):
            d = direcciones[j]
            pinPosible = ()
            for i in range(1, 8):
                endRow = startRow + d[0] * i
                endCol = startCol + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPieza = self.tabla[endRow][endCol]

                    if endPieza[0] == colorAliado and endPieza[1] != 'K':
                        if pinPosible == ():
                            pinPosible = (endRow, endCol, d[0], d[1])
                        else:
                            break
                    elif endPieza[0] == colorEnemigo:
                        tipo = endPieza[1]

                        if (0 <= j <= 3 and tipo == 'R') or \
                                (4 <= j <= 7 and tipo == 'B') or \
                                (i == 1 and tipo == 'p' and (
                                        (colorEnemigo == 'w' and 6 <= j <= 7) or (colorEnemigo == 'b' and 4 <= j <= 5))) or \
                                (tipo == 'Q') or \
                                (i == 1 and tipo == 'K'):
                            if pinPosible == ():
                                enCheck = True
                                checks.append((endRow, endCol, d[0], d[1]))
                                break

                            else:
                                pins.append(pinPosible)
                                break

                        else:
                            break
                else:
                    break

        caballoMovis = ((-2, -1), (-2, 1), (2, -1), (2, 1), (1, 2), (1, -2), (-1, 2), (-1, -2))
        for m in caballoMovis:
            endRow = startRow + m[0]
            endCol = startCol + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPieza = self.tabla[endRow][endCol]
                if endPieza[0] == colorEnemigo and endPieza[1] == 'N':
                    enCheck = True
                    checks.append((endRow, endCol, m[0], m[1]))

        return enCheck, pins, checks, (startRow, startCol)

    def enCheck(self):
        if self.moverParaBlanco:
            return self.cuadEnAtaque(self.localReyBlanco[0], self.localReyBlanco[1])
        else:
            return self.cuadEnAtaque(self.localReyNegro[0], self.localReyNegro[1])

    def cuadEnAtaque(self, r, c):
        self.moverParaBlanco = not self.moverParaBlanco
        opMovis = self.getTodoMovis()
        self.moverParaBlanco = not self.moverParaBlanco

        for movi in opMovis:
            if movi.endRow == r and movi.endCol == c:
                return True

        return False

    def getPeonMov(self, r, c, movis):
        piezaPin = False
        pinDireccion = ()

        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piezaPin = True
                pinDireccion = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        if self.moverParaBlanco:
            cantidadMov = -1
            startRow = 6
            backRow = 0
            colorEnemigo = 'b'
            reyRow, reyCol = self.localReyBlanco

        else:
            cantidadMov = 1
            startRow = 1
            backRow = 7
            colorEnemigo = 'w'
            reyRow, reyCol = self.localReyNegro

        peonPromocion = False

        if self.tabla[r + cantidadMov][c] == '--':
            if not piezaPin or pinDireccion == (cantidadMov, 0):
                if r + cantidadMov == backRow:
                    peonPromocion = True
                movis.append(Movi((r, c), (r + cantidadMov, c), self.tabla, peonPromocion=peonPromocion))

                if r == startRow and self.tabla[r + 2 * cantidadMov][c] == '--':
                    movis.append(Movi((r, c), (r + 2 * cantidadMov, c), self.tabla))

        if c - 1 >= 0:
            if not piezaPin or pinDireccion == (cantidadMov, -1):
                if self.tabla[r + cantidadMov][c - 1][0] == colorEnemigo:
                    if r + cantidadMov == backRow:
                        peonPromocion = True
                    movis.append(Movi((r, c), (r + cantidadMov, c - 1), self.tabla, peonPromocion=peonPromocion))

                if (r + cantidadMov, c - 1) == self.enpassantPosible:
                    piezaAtaque = piezaBloqueo = False
                    if reyRow == r:
                        if reyCol < c:
                            rangoAdentro = range(reyCol + 1, c - 1)
                            rangoAfuera = range(c + 1, 8)
                        else:
                            rangoAdentro = range(reyCol - 1, c, -1)
                            rangoAfuera = range(c - 2, -1, -1)

                        for i in rangoAdentro:
                            if self.tabla[r][i] != '--':
                                piezaBloqueo = True
                        for i in rangoAfuera:
                            cuadrado = self.tabla[r][i]
                            if cuadrado[0] == colorEnemigo and (cuadrado[1] == 'R' or cuadrado[1] == 'Q'):
                                piezaAtaque = True
                            elif cuadrado != '--':
                                piezaBloqueo = True
                    if not piezaAtaque or piezaBloqueo:
                        movis.append(Movi((r, c), (r + cantidadMov, c - 1), self.tabla, enPassant=True))

        if c + 1 <= 7:
            if not piezaPin or pinDireccion == (cantidadMov, 1):
                if self.tabla[r + cantidadMov][c + 1][0] == colorEnemigo:
                    if r + cantidadMov == backRow:
                        peonPromocion = True
                    movis.append(Movi((r, c), (r + cantidadMov, c + 1), self.tabla, peonPromocion=peonPromocion))

                if (r + cantidadMov, c + 1) == self.enpassantPosible:
                    piezaAtaque = piezaBloqueo = False
                    if reyRow == r:
                        if reyCol < c:
                            rangoAdentro = range(reyCol + 1, c)
                            rangoAfuera = range(c + 2, 8)
                        else:
                            rangoAdentro = range(reyCol - 1, c + 1, -1)
                            rangoAfuera = range(c - 1, -1, -1)

                        for i in rangoAdentro:
                            if self.tabla[r][i] != '--':
                                piezaBloqueo = True
                        for i in rangoAfuera:
                            cuadrado = self.tabla[r][i]
                            if cuadrado[0] == colorEnemigo and (cuadrado[1] == 'R' or cuadrado[1] == 'Q'):
                                piezaAtaque = True
                            elif cuadrado != '--':
                                piezaBloqueo = True
                    if not piezaAtaque or piezaBloqueo:
                        movis.append(Movi((r, c), (r + cantidadMov, c + 1), self.tabla, enPassant=True))

    def getTorreMov(self, r, c, movis):
        piezaPin = False
        pinDireccion = ()

        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piezaPin = True
                pinDireccion = (self.pins[i][2], self.pins[i][3])
                if self.tabla[r][c][1] != 'Q':
                    self.pins.remove(self.pins[i])
                break

        direcciones = ((-1, 0), (0, -1), (1, 0), (0, 1))
        colorEnemigo = 'b' if self.moverParaBlanco else 'w'
        for d in direcciones:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    if not piezaPin or pinDireccion == d or pinDireccion == (-d[0], -d[1]):
                        endPieza = self.tabla[endRow][endCol]
                        if endPieza == '--':
                            movis.append(Movi((r, c), (endRow, endCol), self.tabla))
                        elif endPieza[0] == colorEnemigo:
                            movis.append(Movi((r, c), (endRow, endCol), self.tabla))
                            break

                        else:
                            break
                else:
                    break

    def getAlfilMoves(self, r, c, movis):
        piezaPin = False
        pinDireccion = ()

        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piezaPin = True
                pinDireccion = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        direcciones = ((-1, -1), (1, 1), (1, -1), (-1, 1))
        colorEnemigo = 'b' if self.moverParaBlanco else 'w'
        for d in direcciones:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    if not piezaPin or pinDireccion == d or pinDireccion == (-d[0], -d[1]):
                        endPieza = self.tabla[endRow][endCol]
                        if endPieza == '--':
                            movis.append(Movi((r, c), (endRow, endCol), self.tabla))
                        elif endPieza[0] == colorEnemigo:
                            movis.append(Movi((r, c), (endRow, endCol), self.tabla))
                            break
                        else:
                            break
                else:
                    break

    def getCaballoMov(self, r, c, movis):
        piezaPin = False
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piezaPin = True
                self.pins.remove(self.pins[i])
                break

        caballoMovis = ((-2, -1), (-2, 1), (2, -1), (2, 1), (1, 2), (1, -2), (-1, 2), (-1, -2))
        colorAliado = 'w' if self.moverParaBlanco else 'b'
        for m in caballoMovis:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                if not piezaPin:
                    endPieza = self.tabla[endRow][endCol]
                    if endPieza[0] != colorAliado:
                        movis.append(Movi((r, c), (endRow, endCol), self.tabla))

    def getReyMov(self, r, c, movis):
        reyMovis = ((0, 1), (0, -1), (1, 0), (-1, 0), (-1, 1), (-1, -1), (1, 1), (1, -1))
        colorAliado = 'w' if self.moverParaBlanco else 'b'
        for i in range(8):
            endRow = r + reyMovis[i][0]
            endCol = c + reyMovis[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPieza = self.tabla[endRow][endCol]

                if endPieza[0] != colorAliado:
                    if colorAliado == 'w':
                        self.localReyBlanco = (endRow, endCol)
                    else:
                        self.localReyNegro = (endRow, endCol)
                    enCheck, pins, checks, ally = self.verPinsYChecks()

                    if not enCheck:
                        movis.append(Movi((r, c), (endRow, endCol), self.tabla))

                    if colorAliado == 'w':
                        self.localReyBlanco = (r, c)
                    else:
                        self.localReyNegro = (r, c)

    def getReinaMov(self, r, c, movis):
        self.getTorreMov(r, c, movis)
        self.getAlfilMoves(r, c, movis)

    def getEnroqueMov(self, r, c, movis, colorAliado):
        if self.cuadEnAtaque(r, c):
            return
        if (self.moverParaBlanco and self.actualEnroqueDer.wks) or (
                not self.moverParaBlanco and self.actualEnroqueDer.bks):
            self.getReyEnroqueMov(r, c, movis, colorAliado)

        if (self.moverParaBlanco and self.actualEnroqueDer.wqs) or (
                not self.moverParaBlanco and self.actualEnroqueDer.bqs):
            self.getReinaEnroqueMov(r, c, movis, colorAliado)

    def getReyEnroqueMov(self, r, c, movis, colorAliado):
        if self.tabla[r][c + 1] == '--' and self.tabla[r][c + 2] == '--':
            if not self.cuadEnAtaque(r, c + 1) and not self.cuadEnAtaque(r, c + 2):
                movis.append(Movi((r, c), (r, c + 2), self.tabla, esEnroqueMov=True))
            pass

    def getReinaEnroqueMov(self, r, c, movis, colorAliado):
        if self.tabla[r][c - 1] == '--' and self.tabla[r][c - 2] == '--' and self.tabla[r][c - 3] == '--':
            if not self.cuadEnAtaque(r, c - 1) and not self.cuadEnAtaque(r, c - 2):
                movis.append(Movi((r, c), (r, c - 2), self.tabla, esEnroqueMov=True))


class Movi():
    ranksToRows = {'1': 7, '2': 6, '3': 5, '4': 4,
                   '5': 3, '6': 2, '7': 1, '8': 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}

    filesToCols = {'a': 0, 'b': 1, 'c': 2, 'd': 3,
                   'e': 4, 'f': 5, 'g': 6, 'h': 7}

    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, tabla, enPassant=False, peonPromocion=False, esEnroqueMov=False):
        self.startSq = startSq
        self.endSq = endSq
        self.startRow = int(startSq[0])
        self.startCol = int(startSq[1])
        self.endRow = int(endSq[0])
        self.endCol = int(endSq[1])
        self.piezMov = tabla[self.startRow][self.startCol]
        self.piezCap = tabla[self.endRow][self.endCol]
        self.peonPromocion = peonPromocion
        self.moviID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        self.esEnroqueMov = esEnroqueMov

        self.esPeonPromocion = False
        if (self.piezMov == 'wp' and self.endRow == 0) or (self.piezMov == 'bp' and self.endRow == 7):
            self.esPeonPromocion = True

        self.enPassant = enPassant
        if self.enPassant:
            self.piezCap = 'wp' if self.piezMov == 'bp' else 'bp'

    def __eq__(self, other):
        if isinstance(other, Movi):
            return self.moviID == other.moviID
        return False

    def getAjedNot(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]


class EnroqueDer():
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs