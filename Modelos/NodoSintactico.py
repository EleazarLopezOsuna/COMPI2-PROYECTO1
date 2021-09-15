class NodoSintactico():

    # Constructor de la clase nodo
    def __init__(self, nombre, valor, linea, columna):
        self.nombre = nombre
        self.valor = valor
        self.hijos = []
        self.linea = linea
        self.columna = columna
    
    # Agrega un hijo
    def addHijo(self, hijo):
        self.hijos.push(hijo)
    
    # Setea el nombre
    def getNombre(self):
        return str(self.nombre)

    # Obtiene los hijos
    def getHijos(self):
        return self.hijos

    # Obtiene su valor
    def getValor(self):
        return self.valor