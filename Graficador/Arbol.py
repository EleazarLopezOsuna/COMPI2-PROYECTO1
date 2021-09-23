import graphviz

class Arbol():

    # Constructor, no se manda ningun parametro
    def __init__(self):
        self.grafo = ""
        self.contador = 0
        self.dot = graphviz.Digraph(name="grafo", format='svg')
        self.dot.attr('node', shape='box')

    # Generamos la estructura inicial del documento dot
    def getDot(self, raiz):
        self.grafo = 'digraph G{ '
        self.grafo += 'node[shape="box"]; '
        self.contador = 1
        self.grafo += self.graficarNodo(raiz)
        self.grafo += '}'
        return self.grafo, self.dot

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
                self.dot.node(nodo.getNumero() + "_" + nodo.getNombre(), nodo.getValor())
                self.dot.node(hijos.getNumero() + "_" + hijos.getNombre(), hijos.getValor())
                self.dot.edge(nodo.getNumero() + "_" + nodo.getNombre(), hijos.getNumero() + "_" + hijos.getNombre())
                cadena += self.graficarNodo(hijos)
        return cadena
