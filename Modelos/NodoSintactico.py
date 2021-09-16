class NodoSintactico():

    # Constructor de la clase nodo
    def __init__(self, nombre, valor, linea, columna, numero):
        self.nombre = nombre
        self.valor = valor
        self.hijos = []
        self.linea = linea
        self.columna = columna
        self.numero = numero
    
    # Agrega un hijo
    def addHijo(self, hijo):
        self.hijos.append(hijo)
    
    # Setea el nombre
    def getNombre(self):
        return str(self.nombre)

    # Obtiene los hijos
    def getHijos(self):
        return self.hijos

    # Obtiene su valor
    def getValor(self):
        return str(self.valor)
    
    def getNumero(self):
        return str(self.numero)

    def getHijo(self, posicion):
        return self.hijos[posicion]

    def getLinea(self):
        return self.linea

    def getColumna(self):
        return self.columna