from Clases.Abstracto import Abstracto


class Token(Abstracto):
    def __init__(self, token: str, lexema: str, fila: int, columna: int):
        self.token = token
        self.lexema = lexema
        super().__init__(fila, columna)

    def getToken(self):
        return self.token

    def getLexema(self):
        return self.lexema

    def getFila(self):
        return self.fila

    def getColumna(self):
        return self.columna
