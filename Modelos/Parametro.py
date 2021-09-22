class Parametro():

    def __init__(self, nombre, simbolo):
        self.nombre = nombre
        self.simbolo = simbolo
    
    def getNombre(self):
        return str(self.nombre)

    def getSimbolo(self):
        return self.simbolo