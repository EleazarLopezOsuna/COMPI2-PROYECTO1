from Modelos.Simbolo import Simbolo
from Modelos.Simbolo import EnumTipo

class SubPrograma():

    def __init__(self, root, entorno, linea, columna, indexParametros):
        self.root = root
        self.entorno = entorno
        self.retorno = Simbolo(EnumTipo.nulo, "", linea, columna)
        self.entorno.insertar("retorno", self.retorno)
        self.indexParametros = indexParametros

    def getEntorno(self):
        return self.entorno

    def getRoot(self):
        return self.root

    def recibirParametros(self, parametros):
        contador = 0
        for parametro in parametros:
            expresion = parametros[parametro]
            nombreParametro = self.indexParametros[contador]
            self.entorno.modificar(nombreParametro, Simbolo(expresion.getTipo(), expresion.getValor(), -1, -1))
            contador += 1

    def regresarReferencias(self, entornoGlobal, parametros):
        contador = 0
        for parametro in parametros:
            expresion = parametros[parametro]
            if 'expresion2997_' not in parametro:
                if ((expresion.getTipo() == EnumTipo.arreglo) or (expresion.getTipo() == EnumTipo.mutable) or (expresion.getTipo() == EnumTipo.nomutable)):
                    nombreParametro = self.indexParametros[contador]
                    simbolo = self.entorno.buscar(nombreParametro)
                    entornoGlobal.modificar(parametro, simbolo)
            contador += 1
    
    def concatItems(self, simbolo):
        retorno = ""
        for sim in simbolo.getValor():
            if sim.getTipo() == EnumTipo.arreglo:
                cadena = "[" + self.concatItems(sim) + "]"
                if len(retorno) == 0:
                    retorno = cadena
                else:
                    retorno = retorno + ", " + cadena
            else:
                if len(retorno) == 0:
                    retorno = str(sim.getValor())
                else:
                    retorno = retorno + ", " + str(sim.getValor())
        return retorno

    def concatAtributos(self, simbolo):
        retorno = ""
        ent = simbolo.getValor()
        for item in ent.tabla:
            if len(retorno) == 0:
                retorno = str(item)
            else:
                retorno = retorno + ", " + str(item)
        return retorno

    def imprimirEntorno(self, entorno):
        for key in entorno.tabla:
            simbolo = entorno.tabla[key]
            if simbolo.getTipo() == EnumTipo.error:
                print('Entorno: ' + entorno.getNombre() +' Nombre: ' + key + ' Tipo: ' + str(simbolo.getTipo()) + ' Valor: ' + str(simbolo.getValor().getError()) + ' Fila: ' + simbolo.getFila() + ' Columna: ' + simbolo.getColumna())
            elif simbolo.getTipo() == EnumTipo.mutable or simbolo.getTipo() == EnumTipo.nomutable:
                cadena = "{" + self.concatAtributos(simbolo) + "}"
                print('Entorno: ' + entorno.getNombre() +' Nombre: ' + key + ' Tipo: ' + str(simbolo.getTipo()) + ' Valor: ' + cadena + ' Fila: ' + simbolo.getFila() + ' Columna: ' + simbolo.getColumna())
            elif simbolo.getTipo() == EnumTipo.arreglo:
                cadena = "[" + self.concatItems(simbolo) + "]"
                print('Entorno: ' + entorno.getNombre() +' Nombre: ' + key + ' Tipo: ' + str(simbolo.getTipo()) + ' Valor: ' + cadena + ' Fila: ' + simbolo.getFila() + ' Columna: ' + simbolo.getColumna())
            elif simbolo.getTipo() == EnumTipo.funcion:
                print('Entorno: ' + entorno.getNombre() +' Nombre: ' + key + ' Tipo: ' + str(simbolo.getTipo()) + ' Valor: ' + ' Fila: ' + simbolo.getFila() + ' Columna: ' + simbolo.getColumna())
                self.imprimirEntorno(simbolo.getValor().getEntorno())
            else:
                print('Entorno: ' + entorno.getNombre() +' Nombre: ' + key + ' Tipo: ' + str(simbolo.getTipo()) + ' Valor: ' + str(simbolo.getValor()) + ' Fila: ' + simbolo.getFila() + ' Columna: ' + simbolo.getColumna())