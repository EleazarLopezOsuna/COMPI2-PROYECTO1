from Modelos.Simbolo import EnumTipo
from Modelos.Simbolo import Simbolo
class Entorno():

    # Constructor de la clase, nos solicita un entorno anterior. El entorno global tendra como anterior None
    def __init__(self, anterior, nombre):
        self.tabla = {}
        self.anterior = anterior
        self.nombre = nombre

    # Funcion que inserta un variable dentro de nuestro entorno
    def insertar(self, nombre, simbolo):
        if(nombre in self.tabla):
            self.modificar(nombre, simbolo)
        self.tabla[nombre] = simbolo

    # Funcion que busca una variable entre el entorno y sus padres y devuelve su valor 
    # {Objeto: Se encontro, None: no se encontro}
    def buscar(self, nombre):
        actual = self
        while actual != None:
            if nombre in actual.tabla:
                return actual.tabla[nombre]
            else:
                actual = actual.anterior
        return None

    # Funcion que permite saber si una identificador hace referencia a un struct
    # {Objeto: Si es struct y lo devuelve, None: no se encontro o no es struct}
    def isStruct(self, nombre):
        actual = self
        while actual != None:
            if nombre in actual.tabla:
                simbolo = actual.tabla[nombre]
                if((simbolo.getTipo() == EnumTipo.mutable) or (simbolo.getTipo() == EnumTipo.nomutable)):
                    return simbolo
            actual = actual.anterior
        return None

    # Funcion que permite saber si una identificador hace referencia a un arreglo
    # {Objeto: Si es arreglo y lo devuelve, None: no se encontro o no es arreglo}
    def isArreglo(self, nombre):
        actual = self
        while actual != None:
            if nombre in actual.tabla:
                simbolo = actual.tabla[nombre]
                if(simbolo.getTipo() == EnumTipo.arreglo):
                    return simbolo
            actual = actual.anterior
        return None

    # Funcion que busca una variable dentro del entorno y sus padres y modifica su valor
    def modificar(self, nombre, valor):
        actual = self
        while actual != None:
            if nombre in actual.tabla:
                actual.tabla[nombre] = valor
                break
            else:
                actual = actual.anterior
        
    def getNombre(self):
        return str(self.nombre)