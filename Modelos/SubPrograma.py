from Modelos.Simbolo import Simbolo
from Modelos.Simbolo import EnumTipo

class SubPrograma():

    def __init__(self, root, entorno, linea, columna, indexParametros):
        self.nombreParametros = {}
        self.root = root
        self.entorno = entorno
        self.retorno = Simbolo(EnumTipo.nulo, "", linea, columna)
        self.entorno.insertar("retorno", self.retorno)
        self.indexParametros = indexParametros
        self.insertarValorParametro()

    def getEntorno(self):
        return self.entorno

    def getRoot(self):
        return self.root

    def insertarValorParametro(self):
        print(self.indexParametros)
