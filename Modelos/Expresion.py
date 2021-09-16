class Expresion():

    # Constructor clase expresion
    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor = valor

    def getValor(self):
        return self.valor

    def getTipo(self):
        return self.tipo