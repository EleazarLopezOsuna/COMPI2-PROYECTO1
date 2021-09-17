from enum import Enum

class Simbolo():
    
    # Constructor, pide tipo y valor
    def __init__(self, tipo, valor, fila, columna):
        self.tipo = tipo
        self.valor = valor
        self.fila = fila
        self.columna = columna
    
    def getTipo(self):
        return self.tipo
    
    def getValor(self):
        return self.valor

    def getFila(self):
        return str(self.fila)
    
    def getColumna(self):
        return str(self.columna)

# Define los tipos de simbolos
class EnumTipo(Enum):
    arreglo = 1
    caracter = 2
    cadena = 3
    entero = 4
    flotante = 5
    boleano = 6
    nulo = 7
    error = 8
    funcion = 9
    mutable = 10
    nomutable = 11