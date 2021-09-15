class Error():

    # Constructor de la clase error
    def __init__(self, fila, columna, tipo, error):
        self.fila = fila
        self.columna = columna
        self.tipo = tipo
        self.error = error

    # Funciones Getter
    def getFila(self):
        return self.fila
    
    def getColumna(self):
        return self.columna

    def getTipo(self):
        return self.tipo
    
    def getError(self):
        return self.error