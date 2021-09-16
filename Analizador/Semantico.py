from enum import Enum
from Modelos.Entorno import Entorno
from Modelos.Simbolo import Simbolo
from Modelos.Simbolo import EnumTipo
from Modelos.Expresion import Expresion
from Modelos.Objeto import Objeto
from Modelos.NodoSintactico import NodoSintactico
from Modelos.Error import Error
import math

class Semantico():
    def __init__(self, root):
        self.root = root
        self.consola = []
        self.errores = []
        self.entornos = []
        self.entornoGlobal = Entorno(None, "Global")
        self.parar = False
        self.continuar = False
        self.retorno = None
    
    def iniciarAnalisisSemantico(self):
        self.entornos.append(self.entornoGlobal)
        self.retorno = Expresion(EnumTipo.nulo, "")
        self.recorrer(self.root, self.entornoGlobal)

    def recorrer(self, root, entorno):
        if((not self.parar) and (not self.continuar)):
            nuevoEntorno = Entorno
            simbolo = Simbolo
            expresion = Expresion
            llamarHijos = [
                "INICIO",
                "INSTRUCCION"
            ]
            # Switch con ifs
            if(root.getNombre() in llamarHijos):
                for hijo in root.hijos:
                    self.recorrer(hijo, entorno)
            if(root.getNombre() == "LLAMADAFUNCION"):
                #print("")
                self.ejecutarLlamadaFuncion(root, entorno)

    def ejecutarLlamadaFuncion(self, root, entorno):
        nombreFuncion = root.getHijo(0)
        if(nombreFuncion.getNombre() == "PRINTLN"):
            self.ejecutarPrintln(root.getHijo(2), entorno)
        elif(nombreFuncion.getNombre() == "PRINT"):
            self.ejecutarPrint(root.getHijo(2), entorno)

    def ejecutarPrintln(self, root, entorno):
        for hijo in root.hijos:
            if(hijo.getNombre() == "EXPRESION"):
                resultadoExpresion = self.resolverExpresion(hijo, entorno)
                if(resultadoExpresion.getTipo() != EnumTipo.error):
                    self.consola.append(str(resultadoExpresion.getValor()))

    def ejecutarPrint(self, root, entorno):
        print("Funcion print")

    def resolverExpresion(self, root, entorno):
        tmp = Expresion
        sim = Simbolo
        if(root.getNombre() == "EXPRESION"):
            return self.resolverExpresion(root.getHijo(0), entorno)
        if(root.getNombre() == "RESTA"):
            resultadoPrimero = self.resolverExpresion(root.getHijo(0), entorno)
            resultadoSegundo = self.resolverExpresion(root.getHijo(2), entorno)
            return self.operarResta(resultadoPrimero, resultadoSegundo, entorno, root.getHijo(0).getLinea, root.getHijo(0).getColumna)
        if(root.getNombre() == "SUMA"):
            resultadoPrimero = self.resolverExpresion(root.getHijo(0), entorno)
            resultadoSegundo = self.resolverExpresion(root.getHijo(2), entorno)
            return self.operarSuma(resultadoPrimero, resultadoSegundo, entorno, root.getHijo(0).getLinea, root.getHijo(0).getColumna)
        if(root.getNombre() == "NEGATIVO"):
            resultadoPrimero = self.resolverExpresion(root.getHijo(1), entorno)
            return self.operarNegativo(resultadoPrimero, entorno, root.getHijo(1).getLinea, root.getHijo(1).getColumna)
        if(root.getNombre() == "MULTIPLICACION"):
            resultadoPrimero = self.resolverExpresion(root.getHijo(0), entorno)
            resultadoSegundo = self.resolverExpresion(root.getHijo(2), entorno)
            return self.operarMultiplicacion(resultadoPrimero, resultadoSegundo, entorno, root.getHijo(0).getLinea, root.getHijo(0).getColumna)
        if(root.getNombre() == "DIVISION"):
            resultadoPrimero = self.resolverExpresion(root.getHijo(0), entorno)
            resultadoSegundo = self.resolverExpresion(root.getHijo(2), entorno)
            if(int(resultadoSegundo.getValor()) != 0):
                return self.operarDivision(resultadoPrimero, resultadoSegundo, entorno, root.getHijo(0).getLinea, root.getHijo(0).getColumna)
            else:
                return Expresion(EnumTipo.error, Error(root.getHijo(0).getLinea, root.getHijo(0).getColumna, "Semantico", "Division por 0 no definida"))
        if(root.getNombre() == "POTENCIA"):
            resultadoPrimero = self.resolverExpresion(root.getHijo(0), entorno)
            resultadoSegundo = self.resolverExpresion(root.getHijo(2), entorno)
            return self.operarPotencia(resultadoPrimero, resultadoSegundo, entorno, root.getHijo(0).getLinea, root.getHijo(0).getColumna)
        if(root.getNombre() == "MODULO"):
            resultadoPrimero = self.resolverExpresion(root.getHijo(0), entorno)
            resultadoSegundo = self.resolverExpresion(root.getHijo(2), entorno)
            return self.operarModulo(resultadoPrimero, resultadoSegundo, entorno, root.getHijo(0).getLinea, root.getHijo(0).getColumna)
        if(root.getNombre() == "COSENO"):
            resultadoPrimero = self.resolverExpresion(root.getHijo(2), entorno)
            return self.operarCoseno(resultadoPrimero, entorno, root.getHijo(2).getLinea, root.getHijo(2).getColumna)
        if(root.getNombre() == "SENO"):
            resultadoPrimero = self.resolverExpresion(root.getHijo(2), entorno)
            return self.operarSeno(resultadoPrimero, entorno, root.getHijo(2).getLinea, root.getHijo(2).getColumna)
        if(root.getNombre() == "TANGENTE"):
            resultadoPrimero = self.resolverExpresion(root.getHijo(2), entorno)
            return self.operarTangente(resultadoPrimero, entorno, root.getHijo(2).getLinea, root.getHijo(2).getColumna)
        if(root.getNombre() == "ENTERO"):
            return Expresion(EnumTipo.entero, root.getValor())
        if(root.getNombre() == "CADENA"):
            return Expresion(EnumTipo.cadena, root.getValor())
        if(root.getNombre() == "CARACTER"):
            return Expresion(EnumTipo.caracter, root.getValor())
        if(root.getNombre() == "FLOTANTE"):
            return Expresion(EnumTipo.flotante, root.getValor())
        if(root.getNombre() == "NOTHING"):
            return Expresion(EnumTipo.nulo, None)
        if(root.getNombre() == "FALSE"):
            return Expresion(EnumTipo.boleano, True)
        if(root.getNombre() == "TRUE"):
            return Expresion(EnumTipo.boleano, False)

    def operarResta(self, primero, segundo, entorno, linea, columna):
        if(primero.getTipo() == EnumTipo.entero):
            # Entero - Entero = Entero
            if(segundo.getTipo() == EnumTipo.entero):
                return Expresion(EnumTipo.entero, int(primero.getValor()) - int(segundo.getValor()))
            # Entero - Flotante = Flotante
            elif(segundo.getTipo() == EnumTipo.entero):
                return Expresion(EnumTipo.flotante, float(primero.getValor()) - float(segundo.getValor()))
            else:
                return Expresion(EnumTipo.error, Error(linea, columna, "Semantico", "Resta no definida entre los tipos " + str(primero.getTipo()) + " y " + str(segundo.getTipo())))
        elif(primero.getTipo() == EnumTipo.flotante):
            # Flotante - Entero = Flotante
            if(segundo.getTipo() == EnumTipo.entero):
                return Expresion(EnumTipo.flotante, float(primero.getValor()) - float(segundo.getValor()))
            # Flotante - Flotante = Flotante
            elif(segundo.getTipo() == EnumTipo.flotante):
                return Expresion(EnumTipo.flotante, float(primero.getValor()) - float(segundo.getValor()))
            else:
                return Expresion(EnumTipo.error, Error(linea, columna, "Semantico", "Resta no definida entre los tipos " + str(primero.getTipo()) + " y " + str(segundo.getTipo())))
        else:
            return Expresion(EnumTipo.error, Error(linea, columna, "Semantico", "Resta no definida entre los tipos " + str(primero.getTipo()) + " y " + str(segundo.getTipo())))

    def operarNegativo(self, primero, entorno, linea, columna):
        if(primero.getTipo() == EnumTipo.entero):
            # -Entero = Entero
            return Expresion(EnumTipo.entero, int(primero.getValor()) * -1)
        elif(primero.getTipo() == EnumTipo.flotante):
            # -Flotante = Flotante
            return Expresion(EnumTipo.flotante, float(primero.getValor()) * -1)
        else:
            return Expresion(EnumTipo.error, Error(linea, columna, "Semantico", "La operacion negativo no esta definido para el tipo " + str(primero.getTipo())))

    def operarSuma(self, primero, segundo, entorno, linea, columna):
        if(primero.getTipo() == EnumTipo.entero):
            # Entero + Entero = Entero
            if(segundo.getTipo() == EnumTipo.entero):
                return Expresion(EnumTipo.entero, int(primero.getValor()) + int(segundo.getValor()))
            # Entero + Flotante = Flotante
            elif(segundo.getTipo() == EnumTipo.flotante):
                return Expresion(EnumTipo.flotante, float(primero.getValor()) + float(segundo.getValor()))
            else:
                return Expresion(EnumTipo.error, Error(linea, columna, "Semantico", "Suma no definida entre los tipos " + str(primero.getTipo()) + " y " + str(segundo.getTipo())))
        elif(primero.getTipo() == EnumTipo.flotante):
            # Flotante + Entero = Flotante
            if(segundo.getTipo() == EnumTipo.entero):
                return Expresion(EnumTipo.flotante, float(primero.getValor()) + float(segundo.getValor()))
            # Flotante + Flotante = Flotante
            elif(segundo.getTipo() == EnumTipo.flotante):
                return Expresion(EnumTipo.flotante, float(primero.getValor()) + float(segundo.getValor()))
            else:
                return Expresion(EnumTipo.error, Error(linea, columna, "Semantico", "Suma no definida entre los tipos " + str(primero.getTipo()) + " y " + str(segundo.getTipo())))
        else:
            return Expresion(EnumTipo.error, Error(linea, columna, "Semantico", "Suma no definida entre los tipos " + str(primero.getTipo()) + " y " + str(segundo.getTipo())))

    def operarMultiplicacion(self, primero, segundo, entorno, linea, columna):
        if(primero.getTipo() == EnumTipo.entero):
            # Entero * Entero = Entero
            if(segundo.getTipo() == EnumTipo.entero):
                return Expresion(EnumTipo.entero, int(primero.getValor()) * int(segundo.getValor()))
            # Entero * Flotante = Flotante
            elif(segundo.getTipo() == EnumTipo.flotante):
                return Expresion(EnumTipo.flotante, float(primero.getValor()) * float(segundo.getValor()))
            else:
                return Expresion(EnumTipo.error, Error(linea, columna, "Semantico", "Multiplicacion no definida entre los tipos " + str(primero.getTipo()) + " y " + str(segundo.getTipo())))
        elif(primero.getTipo() == EnumTipo.flotante):
            # Flotante * Entero = Flotante
            if(segundo.getTipo() == EnumTipo.entero):
                return Expresion(EnumTipo.flotante, float(primero.getValor()) * float(segundo.getValor()))
            # Flotante * Flotante = Flotante
            elif(segundo.getTipo() == EnumTipo.flotante):
                return Expresion(EnumTipo.flotante, float(primero.getValor()) * float(segundo.getValor()))
            else:
                return Expresion(EnumTipo.error, Error(linea, columna, "Semantico", "Multiplicacion no definida entre los tipos " + str(primero.getTipo()) + " y " + str(segundo.getTipo())))
        elif(primero.getTipo() == EnumTipo.cadena):
            # Cadena * Cadena = Cadena
            if(segundo.getTipo() == EnumTipo.cadena):
                return Expresion(EnumTipo.cadena, str(primero.getValor()) + str(segundo.getValor()))
            else:
                return Expresion(EnumTipo.error, Error(linea, columna, "Semantico", "Multiplicacion no definida entre los tipos " + str(primero.getTipo()) + " y " + str(segundo.getTipo())))
        else:
            return Expresion(EnumTipo.error, Error(linea, columna, "Semantico", "Multiplicacion no definida entre los tipos " + str(primero.getTipo()) + " y " + str(segundo.getTipo())))

    def operarDivision(self, primero, segundo, entorno, linea, columna):
        if(primero.getTipo() == EnumTipo.entero):
            # Entero / Entero = Flotante
            if(segundo.getTipo() == EnumTipo.entero):
                return Expresion(EnumTipo.flotante, float(primero.getValor()) / float(segundo.getValor()))
            # Entero / Flotante = Flotante
            elif(segundo.getTipo() == EnumTipo.flotante):
                return Expresion(EnumTipo.flotante, float(primero.getValor()) / float(segundo.getValor()))
            else:
                return Expresion(EnumTipo.error, Error(linea, columna, "Semantico", "Division no definida entre los tipos " + str(primero.getTipo()) + " y " + str(segundo.getTipo())))
        elif(primero.getTipo() == EnumTipo.flotante):
            # Flotante / Entero = Flotante
            if(segundo.getTipo() == EnumTipo.entero):
                return Expresion(EnumTipo.flotante, float(primero.getValor()) / float(segundo.getValor()))
            # Flotante / Flotante = Flotante
            elif(segundo.getTipo() == EnumTipo.flotante):
                return Expresion(EnumTipo.flotante, float(primero.getValor()) / float(segundo.getValor()))
            else:
                return Expresion(EnumTipo.error, Error(linea, columna, "Semantico", "Division no definida entre los tipos " + str(primero.getTipo()) + " y " + str(segundo.getTipo())))
        else:
            return Expresion(EnumTipo.error, Error(linea, columna, "Semantico", "Division no definida entre los tipos " + str(primero.getTipo()) + " y " + str(segundo.getTipo())))

    def operarPotencia(self, primero, segundo, entorno, linea, columna):
        if(primero.getTipo() == EnumTipo.entero):
            # Entero ^ Entero = Entero
            if(segundo.getTipo() == EnumTipo.entero):
                return Expresion(EnumTipo.entero, int(primero.getValor()) ** int(segundo.getValor()))
            # Entero ^ Flotante = Flotante
            elif(segundo.getTipo() == EnumTipo.flotante):
                return Expresion(EnumTipo.flotante, float(primero.getValor()) ** float(segundo.getValor()))
            else:
                return Expresion(EnumTipo.error, Error(linea, columna, "Semantico", "Potencia no definida entre los tipos " + str(primero.getTipo()) + " y " + str(segundo.getTipo())))
        elif(primero.getTipo() == EnumTipo.flotante):
            # Flotante ^ Entero = Flotante
            if(segundo.getTipo() == EnumTipo.entero):
                return Expresion(EnumTipo.flotante, float(primero.getValor()) ** float(segundo.getValor()))
            # Flotante ^ Flotante = Flotante
            elif(segundo.getTipo() == EnumTipo.flotante):
                return Expresion(EnumTipo.flotante, float(primero.getValor()) ** float(segundo.getValor()))
            else:
                return Expresion(EnumTipo.error, Error(linea, columna, "Semantico", "Potencia no definida entre los tipos " + str(primero.getTipo()) + " y " + str(segundo.getTipo())))
        elif(primero.getTipo() == EnumTipo.cadena):
            # Cadena ^ Entero = Cadena
            if(segundo.getTipo() == EnumTipo.entero):
                return Expresion(EnumTipo.cadena, str(primero.getValor()) * int(segundo.getValor()))
            else:
                return Expresion(EnumTipo.error, Error(linea, columna, "Semantico", "Potencia no definida entre los tipos " + str(primero.getTipo()) + " y " + str(segundo.getTipo())))
        else:
            return Expresion(EnumTipo.error, Error(linea, columna, "Semantico", "Potencia no definida entre los tipos " + str(primero.getTipo()) + " y " + str(segundo.getTipo())))

    def operarModulo(self, primero, segundo, entorno, linea, columna):
        if(primero.getTipo() == EnumTipo.entero):
            # Entero % Entero = Entero
            if(segundo.getTipo() == EnumTipo.entero):
                return Expresion(EnumTipo.entero, int(primero.getValor()) % int(segundo.getValor()))
            # Entero % Flotante = Flotante
            elif(segundo.getTipo() == EnumTipo.flotante):
                return Expresion(EnumTipo.flotante, float(primero.getValor()) % float(segundo.getValor()))
            else:
                return Expresion(EnumTipo.error, Error(linea, columna, "Semantico", "Modulo no definida entre los tipos " + str(primero.getTipo()) + " y " + str(segundo.getTipo())))
        elif(primero.getTipo() == EnumTipo.flotante):
            # Flotante % Entero = Flotante
            if(segundo.getTipo() == EnumTipo.entero):
                return Expresion(EnumTipo.flotante, float(primero.getValor()) + float(segundo.getValor()))
            # Flotante % Flotante = Flotante
            elif(segundo.getTipo() == EnumTipo.flotante):
                return Expresion(EnumTipo.flotante, float(primero.getValor()) + float(segundo.getValor()))
            else:
                return Expresion(EnumTipo.error, Error(linea, columna, "Semantico", "Modulo no definida entre los tipos " + str(primero.getTipo()) + " y " + str(segundo.getTipo())))
        else:
            return Expresion(EnumTipo.error, Error(linea, columna, "Semantico", "Modulo no definida entre los tipos " + str(primero.getTipo()) + " y " + str(segundo.getTipo())))

    def operarCoseno(self, primero, entorno, linea, columna):
        if(primero.getTipo() == EnumTipo.entero):
            return Expresion(EnumTipo.flotante, math.cos(int(primero.getValor())))
        elif(primero.getTipo() == EnumTipo.flotante):
            return Expresion(EnumTipo.flotante, math.cos(float(primero.getValor())))
        else:
            return Expresion(EnumTipo.error, Error(linea, columna, "Semantico", "Coseno no definido para el tipo " + str(primero.getTipo())))

    def operarSeno(self, primero, entorno, linea, columna):
        if(primero.getTipo() == EnumTipo.entero):
            return Expresion(EnumTipo.flotante, math.sin(int(primero.getValor())))
        elif(primero.getTipo() == EnumTipo.flotante):
            return Expresion(EnumTipo.flotante, math.sin(float(primero.getValor())))
        else:
            return Expresion(EnumTipo.error, Error(linea, columna, "Semantico", "Seno no definido para el tipo " + str(primero.getTipo())))

    def operarTangente(self, primero, entorno, linea, columna):
        print(primero.getValor())
        if(primero.getTipo() == EnumTipo.entero):
            return Expresion(EnumTipo.flotante, math.tan(int(primero.getValor())))
        elif(primero.getTipo() == EnumTipo.flotante):
            return Expresion(EnumTipo.flotante, math.tan(float(primero.getValor())))
        else:
            return Expresion(EnumTipo.error, Error(linea, columna, "Semantico", "Tangente no definido para el tipo " + str(primero.getTipo())))