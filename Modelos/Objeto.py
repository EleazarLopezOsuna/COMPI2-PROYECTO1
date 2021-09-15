class Objeto():

    # Constructor de la clase objeto, funciona como multi constructor ya que se hace una verificacion
    # del tipo de dato que le estamos enviando; Puede ser cadena o un Objeto
    def __init__(self, *args):
        if isinstance(args[0], str):
            self.parametros = {}
            self.arreglo = []
            self.tipo = None
            self.nombreTipo = ""
            self.nombre = args[0]
        elif isinstance(args[0], Objeto):
            self.nombre = args[0].nombre
            self.nombreTipo = args[0].nombreTipo
            self.parametros = {}
            for key in args[0].parametros:
                self.parametros[key] = args[0].parametros[key]
            self.tipo = args[0].tipo
            if not args[0].arreglo:
                self.arreglo = args[0].arreglo
    
    # Busca el nombre de un parametro dentro del objeto
    # {Objeto: Encontro, None: No encontro}
    def buscar(self, nombre):
        if nombre in self.parametros:
            return self.parametros[nombre]
        return None
    
    # Busca por nombre y modifica un parametro dentro del objeto
    # {True: Encontro y modifico, False: No encontro}
    def modificar(self, nombre, simbolo):
        if nombre in self.parametros:
            viejo = self.parametros[nombre]
            if viejo == simbolo.tipo:
                self.parametros[nombre] = simbolo
                return True
        return False