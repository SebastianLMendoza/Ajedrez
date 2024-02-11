"""
Responsable de administrar el estado del juego, y de los movimientos validos.
"""
class EstadoJuego():
    def __init__(self):
        #Tablero de 8x8, cada pieza tiene dos letras (color y pieza en ingles).
        #Los "--" representan espacios vacios.
        self.tabla = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.movFuncion = {'p': self.getPeonMov, 'R': self.getTorreMov,
                           'N': self.getCaballoMov, 'B': self.getAlfilMov,
                           'Q': self.getReinaMov, 'K': self.getReyMov}
        self.moverParaBlanco = True
        self.movRegis = []

    def realMov(self, movi):
        self.tabla[movi.startRow][movi.startCol] = "--"
        self.tabla[movi.endRow][movi.endCol] = movi.piezMov
        self.movRegis.append(movi)
        self.moverParaBlanco = not self.moverParaBlanco

    def desMov(self):
        if len(self.movRegis) != 0:
            movi = self.movRegis.pop()
            self.tabla[movi.startRow][movi.startCol] = movi.piezMov
            self.tabla[movi.endRow][movi.endCol] = movi.piezCap
            self.moverParaBlanco = not self.moverParaBlanco

    def getMovValid(self):
        return self.getTodoMov()

    def getTodoMov(self):
        movis = []
        for r in range(len(self.tabla)):
            for c in range(len(self.tabla[r])):
                turno = self.tabla[r][c][0]
                if (turno == 'w' and self.moverParaBlanco) or (turno == 'b' and not self.moverParaBlanco):
                    pieza = self.tabla[r][c][1]
                    self.movFuncion[pieza](r, c, movis)
        return movis

    def getPeonMov(self, r, c, movis):
        if self.moverParaBlanco:
            if self.tabla[r-1][c] == "--":
                movis.append(Movi((r, c), (r-1, c), self.tabla))
                if r == 6 and self.tabla[r-2][c] == "--":
                    movis.append(Movi((r, c), (r-2, c), self.tabla))
            if c-1 >= 0:
                if self.tabla[r-1][c-1][0] == 'b':
                    movis.append(Movi((r, c), (r-1, c-1), self.tabla))
            if c+1 < 7:
                if self.tabla[r-1][c+1][0] == 'b':
                    movis.append(Movi((r, c), (r-1, c+1), self.tabla))
        else:
            if self.tabla[r+1][c] == "--":
                movis.append(Movi((r, c), (r+1, c), self.tabla))
                if r == 1 and self.tabla[r+2][c] == "--":
                    movis.append(Movi((r, c), (r+2, c), self.tabla))
            if c-1 >= 0:
                if self.tabla[r+1][c-1][1] == 'w':
                    movis.append(Movi((r, c), (r+1, c-1), self.tabla))
            if c+1 <= 7:
                if self.tabla[r+1][c+1][1] == 'w':
                    movis.append(Movi((r, c), (r+1, c+1), self.tabla))

    def getTorreMov(self, r, c, movis):
        direcciones = ((-1, 0), (0, -1), (1, 0), (0, 1))
        colorEnemigo = "b" if self.moverParaBlanco else "w"
        for d in direcciones:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPieza = self.tabla[endRow][endCol]
                    if endPieza == "--":
                        movis.append(Movi((r, c), (endRow, endCol), self.tabla))
                    elif endPieza[0] == colorEnemigo:
                        movis.append(Movi((r, c), (endRow, endCol), self.tabla))
                        break
                    else:
                        break
                else:
                    break


    def getCaballoMov(self, r, c, movis):
        caballoMov = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        colorAliado = "w" if self.moverParaBlanco else "b"
        for m in caballoMov:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPieza = self.tabla[endRow][endCol]
                if endPieza[0] != colorAliado:
                    movis.append(Movi((r, c), (endRow, endCol), self.tabla))

    def getAlfilMov(self, r, c, movis):
        direcciones = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        colorEnemigo = "b" if self.moverParaBlanco else "w"
        for d in direcciones:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPieza = self.tabla[endRow][endCol]
                    if endPieza == "--":
                        movis.append(Movi((r, c), (endRow, endCol), self.tabla))
                    elif endPieza[0] == colorEnemigo:
                        movis.append(Movi((r, c), (endRow, endCol), self.tabla))
                        break
                    else:
                        break
                else:
                    break

    def getReinaMov(self, r, c, movis):
        self.getTorreMov(r, c, movis)
        self.getAlfilMov(r, c, movis)

    def getReyMov(self, r, c, movis):
        reyMov = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        colorAliado = "w" if self.moverParaBlanco else "b"
        for i in range(8):
            endRow = r + reyMov[i][0]
            endCol = c + reyMov[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPieza = self.tabla[endRow][endCol]
                if endPieza[0] != colorAliado:
                    movis.append(Movi((r, c), (endRow, endCol), self.tabla))

class Movi():
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, tabla):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.piezMov = tabla[self.startRow][self.startCol]
        self.piezCap = tabla[self.endRow][self.endCol]
        self.moviID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    def __eq__(self, other):
        if isinstance(other, Movi):
            return self.moviID == other.moviID
        return False

    def getAjedNot(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c], self.rowsToRanks[r]