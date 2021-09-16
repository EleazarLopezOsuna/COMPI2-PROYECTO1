class Entorno():

    # Constructor de la clase, nos solicita un entorno anterior. El entorno global tendra como anterior None
    def __init__(self, anterior, nombre):
        self.tabla = {}
        self.anterior = anterior
        self.nombre = nombre

    # Funcion que inserta un variable dentro de nuestro entorno {True: Insertado, False: Error}
    def insertar(self, nombre, simbolo):
        if(nombre in self.tabla):
            return False
        self.tabla[nombre] = simbolo
        return True

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

    # Funcion que busca una variable dentro del entorno y sus padres y modifica su valor
    # {True: Encontro y modifico, False: No lo encontro}
    def modificar(self, nombre, valor):
        actual = self
        while actual != None:
            if nombre in actual.tabla:
                actual.tabla[nombre] = valor
                return True
            else:
                actual = actual.anterior
        return False
        