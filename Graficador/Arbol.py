import graphviz

class Arbol():

    # Constructor, no se manda ningun parametro
    def __init__(self):
        self.grafo = ""
        self.contador = 0

    # Generamos la estructura inicial del documento dot
    def getDot(self, raiz):
        self.grafo = 'digraph G{ '
        self.grafo += 'node[shape="box"]; '
        self.contador = 1
        self.grafo += self.graficarNodo(raiz)
        self.grafo += '}'
        return self.grafo

    # Funcion recursiva capaz de recorrer el arbol e ir generando el codigo necesario para poder graficar
    def graficarNodo(self, nodo):
        cadena = ""
        if nodo != None:
            for hijos in nodo.hijos:
                nodoPadre = ''
                nodoHijo = ''
                nodoPadre = '"' + nodo.getNumero() + "_" + nodo.getNombre() + '"' + '[label = "' + nodo.getValor() + '"];'
                nodoHijo = '"' + hijos.getNumero() + "_" + hijos.getNombre() + '"' + '[label = "' + hijos.getValor() + '"];'
                apuntadorPadre = '"' + nodo.getNumero() + "_" + nodo.getNombre() + '"'
                apuntadorHijo = '"' + hijos.getNumero() + "_" + hijos.getNombre() + '"'
                cadena += nodoPadre + ' ' + nodoHijo + ' ' + apuntadorPadre + '->' + apuntadorHijo + '; '
                cadena += self.graficarNodo(hijos)
        return cadena
