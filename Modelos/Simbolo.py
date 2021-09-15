from enum import Enum

class Simbolo():
    
    # Constructor, pide tipo y valor
    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor = valor

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