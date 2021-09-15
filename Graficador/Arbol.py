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
        self.grafo = ""
        cadena = ""
        for hijos in nodo.getHijo():
            nodoPadre = ""
            nodoHijo = ""
            if(nodo.getValor() != None):
                nodoPadre = "\"" + nodo.getNumNodo() + "_" + nodo.getNombre() + "\"" + "[label = \"" + nodo.getValor() + "\"];"
            else:
                nodoPadre = "\"" + nodo.getNumNodo() + "_" + nodo.getNombre() + "\"" + "[label = \"" + nodo.getNombre() + "\"];"
            if(hijos.getValor() != None):
                nodoHijo = "\"" + hijos.getNumNodo() + "_" + hijos.getNombre() + "\"" + "[label = \"" + hijos.getValor() + "\"];"
            else:
                nodoHijo = "\"" + hijos.getNumNodo() + "_" + hijos.getNombre() + "\"" + "[label = \"" + hijos.getNombre() + "\"];"
            apuntadorPadre = "\"" + nodo.getNumNodo() + "_" + nodo.getNombre() + "\""
            apuntadorHijo = "\"" + hijos.getNumNodo() + "_" + hijos.getNombre() + "\""
            cadena += nodoPadre + "\n" + nodoHijo + "\n" + apuntadorPadre + "->" + apuntadorHijo + ";\n"
            cadena += self.graficarNodo(hijos)
        return cadena
