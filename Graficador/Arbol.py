class Arbol():

    # Constructor, no se manda ningun parametro
    def __init__(self):
        self.grafo = ""
        self.contador = 0

    # Generamos la estructura inicial del documento dot
    def getDot(self, raiz):
        self.grafo = "digraph G{\n"
        self.grafo += "node[shape=\"box\"];\n"
        self.contador = 1
        self.grafo += self.graficarNodo(raiz)
        self.grafo += "\n}"
        return self.grafo

    # Funcion recursiva capaz de recorrer el arbol e ir generando el codigo necesario para poder graficar
    def graficarNodo(self, nodo):
        cadena = ""
        print(nodo.getNombre())
        if nodo != None:
            for hijos in nodo.hijos:
                nodoPadre = ""
                nodoHijo = ""
                nodoPadre = "\"" + nodo.getNumero() + "_" + nodo.getNombre() + "\"" + "[label = \"" + nodo.getValor() + "\"];"
                nodoHijo = "\"" + hijos.getNumero() + "_" + hijos.getNombre() + "\"" + "[label = \"" + hijos.getValor() + "\"];"
                apuntadorPadre = "\"" + nodo.getNumero() + "_" + nodo.getNombre() + "\""
                apuntadorHijo = "\"" + hijos.getNumero() + "_" + hijos.getNombre() + "\""
                cadena += nodoPadre + "\n" + nodoHijo + "\n" + apuntadorPadre + "->" + apuntadorHijo + ";\n"
                cadena += self.graficarNodo(hijos)
        return cadena
