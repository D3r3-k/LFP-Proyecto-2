from Clases.Abstracto import Abstracto


class Error(Abstracto):
    def __init__(self, tipo: str, fila: int, columna: int, token: str, descripcion: str):
        self.tipo = tipo
        self.token = token
        self.descripcion = descripcion
        super().__init__(fila, columna)

    def getTipo(self):
        return self.tipo

    def getToken(self):
        return self.token

    def getDescripcion(self):
        return self.descripcion

    def getFila(self):
        return self.fila

    def getColumna(self):
        return self.columna
