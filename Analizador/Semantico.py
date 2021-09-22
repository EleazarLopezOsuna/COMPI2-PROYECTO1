from enum import Enum
from Modelos.Entorno import Entorno
from Modelos.Simbolo import Simbolo
from Modelos.Simbolo import EnumTipo
from Modelos.Expresion import Expresion
from Modelos.Objeto import Objeto
from Modelos.NodoSintactico import NodoSintactico
from Modelos.Error import Error
from Modelos.SubPrograma import SubPrograma
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
                self.ejecutarLlamadaFuncion(root, entorno)
            if(root.getNombre() == "BLOQUEIF"):
                self.ejecutarBloqueIf(root, entorno)
            if(root.getNombre() == "ASIGNACION"):
                self.ejecutarAsignacion(root, entorno)
            if(root.getNombre() == "STRUCT"):
                self.ejecutarStruct(root, entorno, 0)
            if(root.getNombre() == "MUTABLE"):
                self.ejecutarStruct(root.getHijo(1), entorno, 1)
            if(root.getNombre() == "SWHILE"):
                self.ejecutarWhile(root, entorno)
                self.parar = False
                self.continuar = False
            if(root.getNombre() == "INSTRUCCIONBREAK"):
                self.parar = True
            if(root.getNombre() == "INSTRUCCIONCONTINUE"):
                self.continuar = True
            if(root.getNombre() == "FOR"):
                self.ejecutarFor(root, entorno)
            if(root.getNombre() == "DECLARARFUNCION"):
                self.ejecutarDeclararFuncion(root, entorno)

    def ejecutarDeclararFuncion(self, root, entorno):
        nombreFuncion = root.getHijo(1).getValor()
        entornoFuncion = self.definirParametrosFuncion(root.getHijo(3), entorno, nombreFuncion)
        if entornoFuncion != None:
            instruccionesFuncion = root.getHijo(5)
            if entorno.buscar(nombreFuncion) == None:
                # El nombre de la funcion no existe, si se puede generar
                subPrograma = SubPrograma(instruccionesFuncion, entornoFuncion[0], root.getHijo(1).getLinea(), root.getHijo(1).getColumna(), entornoFuncion[1])
                entorno.insertar(nombreFuncion, Simbolo(EnumTipo.funcion, subPrograma, root.getHijo(1).getLinea(), root.getHijo(1).getColumna()))
            else:
                # Reportar error
                print('El identificador ' + str(nombreFuncion) + ' ya esta definido')
        else:
            # Reportar error
            print('Se encontro un parametro repetido')

    def definirParametrosFuncion(self, root, entorno, nombreFuncion):
        retorno = Entorno(entorno, nombreFuncion)
        retorno2 = {}
        indexParametro = 0
        for parametro in root.hijos:
            if parametro.getNombre() == "PARAMETRO":
                print(parametro.getNombre())
                nombreParametro = str(parametro.getHijo(0).getValor())
                if (nombreParametro in retorno.tabla) == True:
                    return None
                retorno.insertar(nombreParametro, Simbolo(EnumTipo.entero, 0, parametro.getHijo(0).getLinea(), parametro.getHijo(0).getColumna()))
                retorno2[indexParametro] = nombreParametro
                indexParametro += 1
        return retorno, retorno2
    
    def ejecutarFor(self, root, entorno):
        if(len(root.hijos) == 7):
            nombreVariable = root.getHijo(1).getValor()
            if(len(root.getHijo(3).hijos) == 3):
                if(root.getHijo(3).getHijo(1).getValor() == ":"):
                    # for i in a:b instrucciones end;
                    valorInicial = self.resolverExpresion(root.getHijo(3).getHijo(0), entorno)
                    valorFinal = self.resolverExpresion(root.getHijo(3).getHijo(2), entorno)
                    if(valorInicial.getTipo() != EnumTipo.error and valorFinal.getTipo() != EnumTipo.error):
                        if(valorInicial.getTipo() == EnumTipo.entero and valorFinal.getTipo()):
                            indexInicial = int(valorInicial.getValor())
                            indexFinal = int(valorFinal.getValor())
                            for i in range(indexInicial, (indexFinal + 1)):
                                entorno.insertar(nombreVariable, Simbolo(EnumTipo.entero, i, root.getHijo(1).getLinea(), root.getHijo(1).getColumna()))
                                self.recorrer(root.getHijo(4), entorno)
                elif(root.getHijo(3).getHijo(1).getValor() == "LISTAEXPRESIONES"):
                    # for i in [items] instrucciones end ;
                    encontroError = False
                    listaExpresiones = []
                    for hijo in root.getHijo(3).getHijo(1).hijos:
                        if hijo.getNombre() == "EXPRESION":
                            expresion = self.resolverExpresion(hijo, entorno)
                            if(expresion.getTipo() == EnumTipo.error):
                                encontroError = True
                                listaExpresiones = expresion
                                break
                            listaExpresiones.append(expresion)
                    if encontroError == False:
                        for expresion in listaExpresiones:
                            entorno.insertar(nombreVariable, Simbolo(expresion.getTipo(), expresion.getValor(), root.getHijo(1).getLinea(), root.getHijo(1).getColumna()))
                            self.recorrer(root.getHijo(4), entorno)
                    else:
                        # Reportar error
                        print("Se encontro un error en listaExpresiones")
            elif(len(root.getHijo(3).hijos) == 1):
                expresion = self.resolverExpresion(root.getHijo(3), entorno)
                if expresion.getTipo() != EnumTipo.error:
                    if expresion.getTipo() == EnumTipo.cadena or expresion.getTipo() == EnumTipo.arreglo:
                        if expresion.getTipo() == EnumTipo.cadena:
                            cadena = str(expresion.getValor())
                            for i in cadena:
                                entorno.insertar(nombreVariable, Simbolo(EnumTipo.cadena, i, root.getHijo(1).getLinea(), root.getHijo(1).getColumna()))
                                self.recorrer(root.getHijo(4), entorno)
                        if expresion.getTipo() == EnumTipo.arreglo:
                            for i in expresion.getValor():
                                entorno.insertar(nombreVariable, Simbolo(i.getTipo(), i.getValor(), root.getHijo(1).getLinea(), root.getHijo(1).getColumna()))
                                self.recorrer(root.getHijo(4), entorno)
                    else:
                        # Reportar Error
                        print('Se esperaba rango(a:b), arreglo([a,b,c,..] o cadena')
                else:
                    # Reportar Error
                    print('Se encontro un error')
                
    def ejecutarWhile(self, root, entorno):
        condicion = self.resolverExpresion(root.getHijo(1), entorno)
        continuar = True
        if condicion.getTipo() != EnumTipo.error:
            if condicion.getTipo() == EnumTipo.boleano:
                continuar = bool(condicion.getValor())
                while(continuar):
                    self.continuar = False
                    self.recorrer(root.getHijo(2), entorno)
                    condicion = self.resolverExpresion(root.getHijo(1), entorno)
                    continuar = bool(condicion.getValor())
                    if self.parar == True:
                        self.parar = False
                        break

    def ejecutarBloqueIf(self, root, entorno):
        condicion = self.resolverExpresion(root.getHijo(1), entorno)
        if(len(root.hijos) == 5): # Es un if
            if(condicion.getTipo() != EnumTipo.error):
                if(condicion.getTipo() == EnumTipo.boleano):
                    if(str(condicion.getValor()) == "True"):
                        self.recorrer(root.getHijo(2), entorno)
        elif(len(root.hijos) == 6):
            verificar = root.getHijo(3)
            if(verificar.getNombre() == "ELSE"): # Es If-else
                if(condicion.getTipo() != EnumTipo.error):
                    if(condicion.getTipo() == EnumTipo.boleano):
                        if(str(condicion.getValor()) == "True"):
                            self.recorrer(root.getHijo(2), entorno)
                        else:
                            self.recorrer(root.getHijo(3).getHijo(1), entorno)
            else:
                condicion = self.resolverExpresion(root.getHijo(1), entorno)
                if(condicion.getTipo() != EnumTipo.error):
                    if(condicion.getTipo() == EnumTipo.boleano):
                        if(str(condicion.getValor()) == "True"):
                            self.recorrer(root.getHijo(2), entorno)
                        else:
                            resultado = self.ejecutarElseIf(verificar, entorno)
                            if(resultado == False):
                                for hijo in verificar.hijos:
                                    if(hijo.getValor() == "ELSEIF"):
                                        resultado = self.ejecutarElseIf(hijo, entorno)
                                        if(resultado == True):
                                            break
                                    if(hijo.getValor() == "ELSE"):
                                        self.recorrer(hijo.getHijo(1), entorno)

    def ejecutarElseIf(self, root, entorno):
        condicion = self.resolverExpresion(root.getHijo(1), entorno)
        if(condicion.getTipo() != EnumTipo.error):
            if(condicion.getTipo() == EnumTipo.boleano):
                if(str(condicion.getValor()) == "True"):
                    self.recorrer(root.getHijo(2), entorno)
                    return True
        return False

    def ejecutarAsignacion(self, root, entorno):
        if(len(root.hijos) == 6):
            nombreVariableNueva = str(root.getHijo(0).getValor())
            valorVariableNueva = self.resolverExpresion(root.getHijo(2), entorno)
            tipoVariableNueva = str(root.getHijo(4).getHijo(0).getNombre())
            if tipoVariableNueva == "INT64":
                tipoVariableNueva = EnumTipo.entero
            elif tipoVariableNueva == "FLOAT64":
                tipoVariableNueva = EnumTipo.flotante
            elif tipoVariableNueva == "BOLEANO":
                tipoVariableNueva = EnumTipo.boleano
            elif tipoVariableNueva == "CHAR":
                tipoVariableNueva = EnumTipo.caracter
            elif tipoVariableNueva == "STRING":
                tipoVariableNueva = EnumTipo.cadena
            if tipoVariableNueva != "IDENTIFICADOR":
                if valorVariableNueva.getTipo() == tipoVariableNueva:
                    entorno.insertar(nombreVariableNueva, Simbolo(valorVariableNueva.getTipo(), valorVariableNueva.getValor(), root.getHijo(0).getLinea(), root.getHijo(0).getColumna()))
                else:
                    # Reportar Error
                    print('Los tipos ' + str(tipoVariableNueva) + ' y ' + str(valorVariableNueva.getTipo()) + ' no coinciden')
            else:
                # Reportar Error
                print('Se esperaba un tipo primitivo y se encontro ' + str(root.getHijo(4).getHijo(0).getValor()))
        elif(len(root.hijos) == 4):
            if(root.getHijo(2).getNombre() == "EXPRESION"):
                nombreVariableNueva = str(root.getHijo(0).getValor())
                valorVariableNueva = self.resolverExpresion(root.getHijo(2), entorno)
                entorno.insertar(nombreVariableNueva, Simbolo(valorVariableNueva.getTipo(), valorVariableNueva.getValor(), root.getHijo(0).getLinea(), root.getHijo(0).getColumna()))
            else:
                print("Asignacion sin valor pero con tipo")
        elif(len(root.hijos) == 5):
            nombreVariableNueva = str(root.getHijo(0).getValor())
            if(root.getHijo(1).getNombre() == "ACCESOFS"):
                print("Asignacion de atributos de un struct")
            elif(root.getHijo(1).getNombre() == "DIMENSION"):
                simbolo = entorno.isArreglo(nombreVariableNueva)
                dimension = root.getHijo(1)
                resultadoExpresion = self.resolverExpresion(root.getHijo(3), entorno)
                if simbolo != None:
                    posiciones = self.ejecutarObtenerDimension(dimension, entorno)
                    if posiciones != None:
                        self.asignarPosicionArreglo(posiciones, simbolo, nombreVariableNueva, resultadoExpresion)
                else:
                    # Reportar Error
                    print('Se esperaba un arreglo')
        elif(len(root.hijos) == 2):
            nombreVariableNueva = str(root.getHijo(0).getValor())
            entorno.insertar(nombreVariableNueva, Simbolo(EnumTipo.nulo, "",  root.getHijo(0).getLinea(), root.getHijo(0).getColumna()))

    def asignarPosicionArreglo(self, posiciones, simbolo, nombreVariableNueva, expresion):
        if len(posiciones) == 1:
            if simbolo.getTipo() == EnumTipo.arreglo:
                if int(posiciones[0]) < len(simbolo.getValor()):
                    simbolo.getValor()[posiciones[0]] = Simbolo(expresion.getTipo(), expresion.getValor(), simbolo.getFila(), simbolo.getColumna())
                    return simbolo
                else:
                    # Reportar Error
                    print('Index fuera de rango')
            else:
                # Reportar Error
                print('Se esperaba arreglo')
        else:
            if simbolo.getTipo() == EnumTipo.arreglo:
                if  int(posiciones[0]) < len(simbolo.getValor()):
                    nuevoPosiciones = posiciones
                    posicionAnterior = posiciones[0]
                    del nuevoPosiciones[0]
                    simbolo.getValor()[posicionAnterior] = self.asignarPosicionArreglo(nuevoPosiciones, simbolo.getValor()[posicionAnterior], nombreVariableNueva, expresion)
                    return simbolo
                else:
                    # Reportar Error
                    print('Index fuera de rango')
            else:
                # Reportar Error
                print('Se esperaba arreglo')
        return None
    
    def obtenerPosicionArreglo(self, posiciones, simbolo):
        if len(posiciones) == 1:
            if simbolo.getTipo() == EnumTipo.arreglo:
                if int(posiciones[0]) < len(simbolo.getValor()):
                    return simbolo.getValor()[posiciones[0]]
                else:
                    return Expresion(EnumTipo.error, Error(simbolo.fila, simbolo.columna, "Semantico", "Index fuera de rango"))
            else:
                return Expresion(EnumTipo.error, Error(simbolo.fila, simbolo.columna, "Semantico", "Se esperaba arreglo"))
        else:
            if simbolo.getTipo() == EnumTipo.arreglo:
                if  int(posiciones[0]) < len(simbolo.getValor()):
                    nuevoPosiciones = posiciones
                    posicionAnterior = posiciones[0]
                    del nuevoPosiciones[0]
                    return self.obtenerPosicionArreglo(nuevoPosiciones, simbolo.getValor()[posicionAnterior])
                else:
                    return Expresion(EnumTipo.error, Error(simbolo.fila, simbolo.columna, "Semantico", "Index fuera de rango"))
            else:
                return Expresion(EnumTipo.error, Error(simbolo.fila, simbolo.columna, "Semantico", "Se esperaba arreglo"))
        return None

    def ejecutarObtenerDimension(self, root, entorno):
        posiciones = []
        for hijo in root.hijos:
            if hijo.getNombre() == "EXPRESION":
                expresion = self.resolverExpresion(hijo, entorno)
                if expresion.getTipo() != EnumTipo.error:
                    if expresion.getTipo() == EnumTipo.entero:
                        posiciones.append(int(expresion.getValor()) - 1)
                    else:
                        # Reportar Error
                        print('Se esperaba tipo entero')
                        return None
                else:
                    # Reportar Error
                    print('Se encontro un error')
                    return None
        return posiciones

    def ejecutarStruct(self, root, entorno, tipo):
        # La expresion es un arreglo
        nuevoEntorno = Entorno(entorno, "")
        nombreStruct = str(root.getHijo(1).getValor())
        for hijo in root.getHijo(2).hijos:
            # Obtengo todos los hijos
            if(hijo.getNombre() == "ATRIBUTO"):
                nombreAtributo = hijo.getHijo(0).getValor()
                nuevoEntorno.insertar(nombreAtributo, Simbolo(EnumTipo.nulo, "", hijo.getHijo(0).getLinea(), hijo.getHijo(0).getColumna()))
        if(tipo == 0):
            entorno.insertar(nombreStruct, Simbolo(EnumTipo.nomutable, nuevoEntorno, root.getHijo(1).getLinea(), root.getHijo(1).getColumna()))
        else:
            entorno.insertar(nombreStruct, Simbolo(EnumTipo.nomutable, nuevoEntorno, root.getHijo(1).getLinea(), root.getHijo(1).getColumna()))

    def ejecutarLlamadaFuncion(self, root, entorno):
        nombreFuncion = root.getHijo(0)
        if(nombreFuncion.getNombre() == "PRINTLN"):
            self.ejecutarPrintln(root.getHijo(2), entorno)
        elif(nombreFuncion.getNombre() == "PRINT"):
            self.ejecutarPrint(root.getHijo(2), entorno)
        else:
            print("OTRA FUNCION")

    def ejecutarPrintln(self, root, entorno):
        cadena = ""
        for hijo in root.hijos:
            if(hijo.getNombre() == "EXPRESION"):
                resultadoExpresion = self.resolverExpresion(hijo, entorno)
                if(resultadoExpresion.getTipo() != EnumTipo.error):
                    cadena += str(resultadoExpresion.getValor())
        self.consola.append(cadena)

    def ejecutarPrint(self, root, entorno):
        for hijo in root.hijos:
            if(hijo.getNombre() == "EXPRESION"):
                resultadoExpresion = self.resolverExpresion(hijo, entorno)
                if(resultadoExpresion.getTipo() != EnumTipo.error):
                    size = len(self.consola)
                    if size != 0:
                        size -= 1
                        texto = self.consola[size]
                        self.consola[size] = texto + str(resultadoExpresion.getValor())
                    else:
                        self.consola.append(str(resultadoExpresion.getValor()))

    def resolverExpresion(self, root, entorno):
        if(root.getNombre() == "EXPRESION"):
            if(len(root.hijos) == 1):
                return self.resolverExpresion(root.getHijo(0), entorno)
            elif((len(root.hijos) == 3) and (root.getHijo(1).getNombre() == "EXPRESION")):
                return self.resolverExpresion(root.getHijo(1), entorno)
            elif((len(root.hijos) == 3) and (root.getHijo(1).getNombre() == "LISTAEXPRESIONES")):
                # La expresion es un arreglo
                retorno = Expresion(EnumTipo.arreglo, [])
                for hijo in root.getHijo(1).hijos:
                    # Obtengo todos los hijos
                    if(hijo.getNombre() == "EXPRESION"):
                        expresion = self.resolverExpresion(hijo, entorno)
                        if(expresion.getTipo() != EnumTipo.error):
                            simbolo = Simbolo(expresion.getTipo(), expresion.getValor(), -1, -1)
                            retorno.valor.append(simbolo)
                        else:
                            # Reportar error
                            print('Se encontro error')
                return retorno
            elif((len(root.hijos) == 2) and (root.getHijo(1).getNombre() == "DIMENSION")):
                nombreVariableNueva = root.getHijo(0).getValor()
                simbolo = entorno.isArreglo(nombreVariableNueva)
                if simbolo != None:
                    posiciones = self.ejecutarObtenerDimension(root.getHijo(1), entorno)
                    if posiciones != None:
                        return self.obtenerPosicionArreglo(posiciones, simbolo)


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
            if(resultadoSegundo.getTipo() == EnumTipo.entero or resultadoSegundo.getTipo() == EnumTipo.flotante):
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
        if(root.getNombre() == "LOGNATURAL"):
            resultadoPrimero = self.resolverExpresion(root.getHijo(2), entorno)
            if(resultadoPrimero.getTipo() == EnumTipo.entero or resultadoPrimero.getTipo() == EnumTipo.flotante):
                if(int(resultadoPrimero.getValor()) > 0):
                    return self.operarLogNatural(resultadoPrimero, entorno, root.getHijo(2).getLinea, root.getHijo(2).getColumna)
                else:
                    return Expresion(EnumTipo.error, Error(root.getHijo(2).getLinea, root.getHijo(2).getColumna, "Semantico", "Rango fuera de limite"))
        if(root.getNombre() == "LOGBASE"):
            resultadoPrimero = self.resolverExpresion(root.getHijo(2), entorno)
            resultadoSegundo = self.resolverExpresion(root.getHijo(4), entorno)
            if((resultadoPrimero.getTipo() == EnumTipo.entero or resultadoPrimero.getTipo() == EnumTipo.flotante) and (resultadoSegundo.getTipo() == EnumTipo.entero or resultadoSegundo.getTipo() == EnumTipo.flotante)):
                if((int(resultadoPrimero.getValor()) > 0) and (int(resultadoSegundo.getValor()) > 0)):
                    return self.operarLogBase(resultadoPrimero, resultadoSegundo, entorno, root.getHijo(2).getLinea, root.getHijo(2).getColumna)
                else:
                    return Expresion(EnumTipo.error, Error(root.getHijo(2).getLinea, root.getHijo(2).getColumna, "Semantico", "Rango fuera de limite"))
        if(root.getNombre() == "RAIZ"):
            resultadoPrimero = self.resolverExpresion(root.getHijo(2), entorno)
            if(resultadoPrimero.getTipo() == EnumTipo.entero or resultadoPrimero.getTipo() == EnumTipo.flotante):
                if(int(resultadoPrimero.getValor()) >= 0):
                    return self.operarRaiz(resultadoPrimero, entorno, root.getHijo(2).getLinea, root.getHijo(2).getColumna)
                else:
                    return Expresion(EnumTipo.error, Error(root.getHijo(2).getLinea, root.getHijo(2).getColumna, "Semantico", "Rango fuera de limite"))
        if(root.getNombre() == "PARSEINT"):
            resultadoPrimero = self.resolverExpresion(root.getHijo(4), entorno)
            return self.operarParseInt(resultadoPrimero, entorno, root.getHijo(4).getLinea, root.getHijo(4).getColumna)
        if(root.getNombre() == "PARSEFLOAT"):
            resultadoPrimero = self.resolverExpresion(root.getHijo(4), entorno)
            return self.operarParseFloat(resultadoPrimero, entorno, root.getHijo(4).getLinea, root.getHijo(4).getColumna)
        if(root.getNombre() == "TRUNCAR"):
            resultadoPrimero = self.resolverExpresion(root.getHijo(2), entorno)
            return self.operarTruncar(resultadoPrimero, entorno, root.getHijo(2).getLinea, root.getHijo(2).getColumna)
        if(root.getNombre() == "HACERUPPERCASE"):
            resultadoPrimero = self.resolverExpresion(root.getHijo(2), entorno)
            return self.operarUppercase(resultadoPrimero, entorno, root.getHijo(2).getLinea, root.getHijo(2).getColumna)
        if(root.getNombre() == "HACERLOWERCASE"):
            resultadoPrimero = self.resolverExpresion(root.getHijo(2), entorno)
            return self.operarLowercase(resultadoPrimero, entorno, root.getHijo(2).getLinea, root.getHijo(2).getColumna)
        if(root.getNombre() == "CONVERTIRFLOAT"):
            resultadoPrimero = self.resolverExpresion(root.getHijo(2), entorno)
            return self.operarParseFloat(resultadoPrimero, entorno, root.getHijo(2).getLinea, root.getHijo(2).getColumna)
        if(root.getNombre() == "OBTENERTIPO"):
            resultadoPrimero = self.resolverExpresion(root.getHijo(2), entorno)
            return self.operarTypeOf(resultadoPrimero, entorno, root.getHijo(2).getLinea, root.getHijo(2).getColumna)
        if(root.getNombre() == "CONVERTIRSTRING"):
            resultadoPrimero = self.resolverExpresion(root.getHijo(2), entorno)
            return self.operarConvertirString(resultadoPrimero, entorno, root.getHijo(2).getLinea, root.getHijo(2).getColumna)
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
            return Expresion(EnumTipo.boleano, False)
        if(root.getNombre() == "TRUE"):
            return Expresion(EnumTipo.boleano, True)
        if(root.getNombre() == "MAYOR"):
            resultadoPrimero = self.resolverExpresion(root.getHijo(0), entorno)
            resultadoSegundo = self.resolverExpresion(root.getHijo(2), entorno)
            return self.operarMayor(resultadoPrimero, resultadoSegundo, entorno, root.getHijo(0).getLinea, root.getHijo(0).getColumna)
        if(root.getNombre() == "MENOR"):
            resultadoPrimero = self.resolverExpresion(root.getHijo(0), entorno)
            resultadoSegundo = self.resolverExpresion(root.getHijo(2), entorno)
            return self.operarMenor(resultadoPrimero, resultadoSegundo, entorno, root.getHijo(0).getLinea, root.getHijo(0).getColumna)
        if(root.getNombre() == "MAYORIGUAL"):
            resultadoPrimero = self.resolverExpresion(root.getHijo(0), entorno)
            resultadoSegundo = self.resolverExpresion(root.getHijo(2), entorno)
            return self.operarMayorIgual(resultadoPrimero, resultadoSegundo, entorno, root.getHijo(0).getLinea, root.getHijo(0).getColumna)
        if(root.getNombre() == "MENORIGUAL"):
            resultadoPrimero = self.resolverExpresion(root.getHijo(0), entorno)
            resultadoSegundo = self.resolverExpresion(root.getHijo(2), entorno)
            return self.operarMenorIgual(resultadoPrimero, resultadoSegundo, entorno, root.getHijo(0).getLinea, root.getHijo(0).getColumna)
        if(root.getNombre() == "IGUALDAD"):
            resultadoPrimero = self.resolverExpresion(root.getHijo(0), entorno)
            resultadoSegundo = self.resolverExpresion(root.getHijo(2), entorno)
            return self.operarIgualdad(resultadoPrimero, resultadoSegundo, entorno, root.getHijo(0).getLinea, root.getHijo(0).getColumna)
        if(root.getNombre() == "DIFERENCIA"):
            resultadoPrimero = self.resolverExpresion(root.getHijo(0), entorno)
            resultadoSegundo = self.resolverExpresion(root.getHijo(2), entorno)
            return self.operarDiferente(resultadoPrimero, resultadoSegundo, entorno, root.getHijo(0).getLinea, root.getHijo(0).getColumna)
        if(root.getNombre() == "OR"):
            resultadoPrimero = self.resolverExpresion(root.getHijo(0), entorno)
            resultadoSegundo = self.resolverExpresion(root.getHijo(2), entorno)
            return self.operarOr(resultadoPrimero, resultadoSegundo, entorno, root.getHijo(0).getLinea, root.getHijo(0).getColumna)
        if(root.getNombre() == "AND"):
            resultadoPrimero = self.resolverExpresion(root.getHijo(0), entorno)
            resultadoSegundo = self.resolverExpresion(root.getHijo(2), entorno)
            return self.operarAnd(resultadoPrimero, resultadoSegundo, entorno, root.getHijo(0).getLinea, root.getHijo(0).getColumna)
        if(root.getNombre() == "NOT"):
            resultadoPrimero = self.resolverExpresion(root.getHijo(0), entorno)
            return self.operarNot(resultadoPrimero, entorno, root.getHijo(0).getLinea, root.getHijo(0).getColumna)
        if(root.getNombre() == "OBTENERSIZE"):
            expresion = self.resolverExpresion(root.getHijo(2), entorno)
            if(expresion.getTipo() != EnumTipo.error):
                if(expresion.getTipo() == EnumTipo.arreglo):
                    return Expresion(EnumTipo.entero, len(expresion.getValor()))
                else:
                    # Reportar Error
                    return Expresion(EnumTipo.error, "Se esperaba un arreglo, se obtuvo " + str(expresion.getTipo()))
            else:
                return expresion
        if(root.getNombre() == "HACERPOP"):
            print("pop")
        if(root.getNombre() == "IDENTIFICADOR"):
            return self.obtenerValorIdentificador(root, entorno, root.getLinea(), root.getColumna())

    def obtenerValorIdentificador(self, root, entorno, linea, columna):
        simbolo = entorno.buscar(str(root.getValor()))
        if simbolo != None:
            return Expresion(simbolo.getTipo(), simbolo.getValor())
        else:
            return Expresion(EnumTipo.error, Error(linea, columna, "Semantico", "La variable " + str(root.getValor()) + " no existe"))

    def operarResta(self, primero, segundo, entorno, linea, columna):
        if(primero.getTipo() == EnumTipo.entero):
            # Entero - Entero = Entero
            if(segundo.getTipo() == EnumTipo.entero):
                return Expresion(EnumTipo.entero, int(primero.getValor()) - int(segundo.getValor()))
            # Entero - Flotante = Flotante
            elif(segundo.getTipo() == EnumTipo.flotante):
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
        if(primero.getTipo() == EnumTipo.entero):
            return Expresion(EnumTipo.flotante, math.tan(int(primero.getValor())))
        elif(primero.getTipo() == EnumTipo.flotante):
            return Expresion(EnumTipo.flotante, math.tan(float(primero.getValor())))
        else:
            return Expresion(EnumTipo.error, Error(linea, columna, "Semantico", "Tangente no definido para el tipo " + str(primero.getTipo())))

    def operarLogNatural(self, primero, entorno, linea, columna):
        if(primero.getTipo() == EnumTipo.entero):
            return Expresion(EnumTipo.flotante, math.log10(int(primero.getValor())))
        elif(primero.getTipo() == EnumTipo.flotante):
            return Expresion(EnumTipo.flotante, math.log10(float(primero.getValor())))
        else:
            return Expresion(EnumTipo.error, Error(linea, columna, "Semantico", "Logaritmo natural no definido para el tipo " + str(primero.getTipo())))

    def operarLogBase(self, primero, segundo, entorno, linea, columna):
        if(primero.getTipo() == EnumTipo.entero):
            if(segundo.getTipo() == EnumTipo.entero):
                return Expresion(EnumTipo.flotante, math.log(int(segundo.getValor()), int(primero.getValor())))
            elif(segundo.getTipo() == EnumTipo.flotante):
                return Expresion(EnumTipo.flotante, math.log(int(segundo.getValor()), float(primero.getValor())))
            else:
                return Expresion(EnumTipo.error, Error(linea, columna, "Semantico", "Logaritmo no definido para los tipos " + str(primero.getTipo()) + " y " + str(segundo.getTipo())))
        elif(primero.getTipo() == EnumTipo.flotante):
            if(segundo.getTipo() == EnumTipo.entero):
                return Expresion(EnumTipo.flotante, math.log(float(segundo.getValor()), int(primero.getValor())))
            elif(segundo.getTipo == EnumTipo.flotante):
                return Expresion(EnumTipo.flotante, math.log(float(segundo.getValor()), float(primero.getValor())))
            else:
                return Expresion(EnumTipo.error, Error(linea, columna, "Semantico", "Logaritmo no definido para los tipos " + str(primero.getTipo()) + " y " + str(segundo.getTipo())))
        else:
            return Expresion(EnumTipo.error, Error(linea, columna, "Semantico", "Logaritmo natural no definido para el tipo " + str(primero.getTipo())))
    
    def operarRaiz(self, primero, entorno, linea, columna):
        if(primero.getTipo() == EnumTipo.entero):
            return Expresion(EnumTipo.flotante, math.sqrt(int(primero.getValor())))
        elif(primero.getTipo() == EnumTipo.flotante):
            return Expresion(EnumTipo.flotante, math.sqrt(float(primero.getValor())))
        else:
            return Expresion(EnumTipo.error, Error(linea, columna, "Semantico", "Raiz no definida para el tipo " + str(primero.getTipo())))

    def operarRaiz(self, primero, entorno, linea, columna):
        if(primero.getTipo() == EnumTipo.entero):
            return Expresion(EnumTipo.flotante, math.sqrt(int(primero.getValor())))
        elif(primero.getTipo() == EnumTipo.flotante):
            return Expresion(EnumTipo.flotante, math.sqrt(float(primero.getValor())))
        else:
            return Expresion(EnumTipo.error, Error(linea, columna, "Semantico", "Raiz no definida para el tipo " + str(primero.getTipo())))
    
    def intTryParse(self, value):
        try:
            int(value)
            return True
        except ValueError:
            return False

    def floatTryParse(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    def operarParseInt(self, primero, entorno, linea, columna):
        if(self.intTryParse(primero.getValor())):
            if(primero.getTipo() == EnumTipo.cadena):
                return Expresion(EnumTipo.entero, int(primero.getValor()))
            elif(primero.getTipo() == EnumTipo.flotante):
                return Expresion(EnumTipo.entero, int(primero.getValor()))
            else:
                return Expresion(EnumTipo.error, Error(linea, columna, "Semantico", "ParseInt no definido para el tipo " + str(primero.getTipo())))
        else:
            return Expresion(EnumTipo.error, Error(linea, columna, "Semantico", "El valor " + str(primero.getValor()) + " no es numerico"))

    def operarParseFloat(self, primero, entorno, linea, columna):
        if(self.floatTryParse(primero.getValor())):
            if(primero.getTipo() == EnumTipo.cadena):
                return Expresion(EnumTipo.flotante, float(primero.getValor()))
            elif(primero.getTipo() == EnumTipo.flotante):
                return Expresion(EnumTipo.flotante, float(primero.getValor()))
            elif(primero.getTipo() == EnumTipo.entero):
                return Expresion(EnumTipo.flotante, float(primero.getValor()))
            else:
                return Expresion(EnumTipo.error, Error(linea, columna, "Semantico", "ParseFloat no definido para el tipo " + str(primero.getTipo())))
        else:
            return Expresion(EnumTipo.error, Error(linea, columna, "Semantico", "El valor " + str(primero.getValor()) + " no es numerico"))

    def operarTruncar(self, primero, entorno, linea, columna):
        if(primero.getTipo() == EnumTipo.flotante):
            return Expresion(EnumTipo.entero, math.trunc(float(primero.getValor())))
        else:
            return Expresion(EnumTipo.error, Error(linea, columna, "Semantico", "Trunc no definido para el tipo " + str(primero.getTipo())))

    def operarUppercase(self, primero, entorno, linea, columna):
        if(primero.getTipo() == EnumTipo.cadena):
            cadena = str(primero.getValor())
            return Expresion(EnumTipo.cadena, cadena.upper())
        else:
            return Expresion(EnumTipo.error, Error(linea, columna, "Semantico", "Uppercase no definido para el tipo " + str(primero.getTipo())))

    def operarLowercase(self, primero, entorno, linea, columna):
        if(primero.getTipo() == EnumTipo.cadena):
            cadena = str(primero.getValor())
            return Expresion(EnumTipo.cadena, cadena.lower())
        else:
            return Expresion(EnumTipo.error, Error(linea, columna, "Semantico", "Lowercase no definido para el tipo " + str(primero.getTipo())))

    def operarTypeOf(self, primero, entorno, linea, columna):
        cadena = ""
        if(primero.getTipo() == EnumTipo.cadena):
            cadena = "string"
        if(primero.getTipo() == EnumTipo.entero):
            cadena = "int"
        if(primero.getTipo() == EnumTipo.flotante):
            cadena = "float"
        if(primero.getTipo() == EnumTipo.caracter):
            cadena = "char"
        if(primero.getTipo() == EnumTipo.arreglo):
            cadena = "array"
        if(primero.getTipo() == EnumTipo.boleano):
            cadena = "bool"
        if(primero.getTipo() == EnumTipo.nulo):
            cadena = "nothing"
        if(primero.getTipo() == EnumTipo.funcion):
            cadena = "function"
        if(primero.getTipo() == EnumTipo.mutable):
            cadena = "struct"
        if(primero.getTipo() == EnumTipo.nomutable):
            cadena = "struct"
        return Expresion(EnumTipo.cadena, cadena)

    def operarConvertirString(self, primero, entorno, linea, columna):
        if(primero.getTipo() != EnumTipo.error):
            return Expresion(EnumTipo.cadena, str(primero.getValor()))
        else:
            return Expresion(EnumTipo.error, Error(linea, columna, "Semantico", "string no definido para el tipo " + str(primero.getTipo())))

    def operarMayor(self, primero, segundo, entorno, linea, columna):
        if(primero.getTipo() == EnumTipo.entero):
            if(segundo.getTipo() == EnumTipo.entero):
                return Expresion(EnumTipo.boleano, int(primero.getValor()) > int(segundo.getValor()))
            elif(segundo.getTipo() == EnumTipo.entero):
                return Expresion(EnumTipo.boleano, float(primero.getValor()) > float(segundo.getValor()))
            else:
                return Expresion(EnumTipo.error, Error(linea, columna, "Semantico", "Mayor que no definido entre los tipos " + str(primero.getTipo()) + " y " + str(segundo.getTipo())))
        elif(primero.getTipo() == EnumTipo.flotante):
            if(segundo.getTipo() == EnumTipo.entero):
                return Expresion(EnumTipo.boleano, float(primero.getValor()) > float(segundo.getValor()))
            elif(segundo.getTipo() == EnumTipo.flotante):
                return Expresion(EnumTipo.boleano, float(primero.getValor()) > float(segundo.getValor()))
            else:
                return Expresion(EnumTipo.error, Error(linea, columna, "Semantico", "Mayor que no definido entre los tipos " + str(primero.getTipo()) + " y " + str(segundo.getTipo())))
        elif(primero.getTipo() == EnumTipo.cadena):
            if(segundo.getTipo() == EnumTipo.cadena):
                return Expresion(EnumTipo.boleano, str(primero.getValor()) > str(segundo.getValor()))
            else:
                return Expresion(EnumTipo.error, Error(linea, columna, "Semantico", "Mayor que no definido entre los tipos " + str(primero.getTipo()) + " y " + str(segundo.getTipo())))
        else:
            return Expresion(EnumTipo.error, Error(linea, columna, "Semantico", "Mayor que no definido entre los tipos " + str(primero.getTipo()) + " y " + str(segundo.getTipo())))

    def operarMenor(self, primero, segundo, entorno, linea, columna):
        if(primero.getTipo() == EnumTipo.entero):
            if(segundo.getTipo() == EnumTipo.entero):
                return Expresion(EnumTipo.boleano, int(primero.getValor()) < int(segundo.getValor()))
            elif(segundo.getTipo() == EnumTipo.entero):
                return Expresion(EnumTipo.boleano, float(primero.getValor()) < float(segundo.getValor()))
            else:
                return Expresion(EnumTipo.error, Error(linea, columna, "Semantico", "Menor que no definido entre los tipos " + str(primero.getTipo()) + " y " + str(segundo.getTipo())))
        elif(primero.getTipo() == EnumTipo.flotante):
            if(segundo.getTipo() == EnumTipo.entero):
                return Expresion(EnumTipo.boleano, float(primero.getValor()) < float(segundo.getValor()))
            elif(segundo.getTipo() == EnumTipo.flotante):
                return Expresion(EnumTipo.boleano, float(primero.getValor()) < float(segundo.getValor()))
            else:
                return Expresion(EnumTipo.error, Error(linea, columna, "Semantico", "Menor que no definido entre los tipos " + str(primero.getTipo()) + " y " + str(segundo.getTipo())))
        elif(primero.getTipo() == EnumTipo.cadena):
            if(segundo.getTipo() == EnumTipo.cadena):
                return Expresion(EnumTipo.boleano, str(primero.getValor()) < str(segundo.getValor()))
            else:
                return Expresion(EnumTipo.error, Error(linea, columna, "Semantico", "Menor que no definido entre los tipos " + str(primero.getTipo()) + " y " + str(segundo.getTipo())))
        else:
            return Expresion(EnumTipo.error, Error(linea, columna, "Semantico", "Menor que no definido entre los tipos " + str(primero.getTipo()) + " y " + str(segundo.getTipo())))

    def operarMayorIgual(self, primero, segundo, entorno, linea, columna):
        if(primero.getTipo() == EnumTipo.entero):
            if(segundo.getTipo() == EnumTipo.entero):
                return Expresion(EnumTipo.boleano, int(primero.getValor()) >= int(segundo.getValor()))
            elif(segundo.getTipo() == EnumTipo.entero):
                return Expresion(EnumTipo.boleano, float(primero.getValor()) >= float(segundo.getValor()))
            else:
                return Expresion(EnumTipo.error, Error(linea, columna, "Semantico", "Mayor o igual que no definido entre los tipos " + str(primero.getTipo()) + " y " + str(segundo.getTipo())))
        elif(primero.getTipo() == EnumTipo.flotante):
            if(segundo.getTipo() == EnumTipo.entero):
                return Expresion(EnumTipo.boleano, float(primero.getValor()) >= float(segundo.getValor()))
            elif(segundo.getTipo() == EnumTipo.flotante):
                return Expresion(EnumTipo.boleano, float(primero.getValor()) >= float(segundo.getValor()))
            else:
                return Expresion(EnumTipo.error, Error(linea, columna, "Semantico", "Mayor o igual que no definido entre los tipos " + str(primero.getTipo()) + " y " + str(segundo.getTipo())))
        elif(primero.getTipo() == EnumTipo.cadena):
            if(segundo.getTipo() == EnumTipo.cadena):
                return Expresion(EnumTipo.boleano, str(primero.getValor()) >= str(segundo.getValor()))
            else:
                return Expresion(EnumTipo.error, Error(linea, columna, "Semantico", "Mayor o igual que no definido entre los tipos " + str(primero.getTipo()) + " y " + str(segundo.getTipo())))
        else:
            return Expresion(EnumTipo.error, Error(linea, columna, "Semantico", "Mayor o igual que no definido entre los tipos " + str(primero.getTipo()) + " y " + str(segundo.getTipo())))

    def operarMenorIgual(self, primero, segundo, entorno, linea, columna):
        if(primero.getTipo() == EnumTipo.entero):
            if(segundo.getTipo() == EnumTipo.entero):
                return Expresion(EnumTipo.boleano, int(primero.getValor()) <= int(segundo.getValor()))
            elif(segundo.getTipo() == EnumTipo.entero):
                return Expresion(EnumTipo.boleano, float(primero.getValor()) <= float(segundo.getValor()))
            else:
                return Expresion(EnumTipo.error, Error(linea, columna, "Semantico", "Menor o igual que no definido entre los tipos " + str(primero.getTipo()) + " y " + str(segundo.getTipo())))
        elif(primero.getTipo() == EnumTipo.flotante):
            if(segundo.getTipo() == EnumTipo.entero):
                return Expresion(EnumTipo.boleano, float(primero.getValor()) <= float(segundo.getValor()))
            elif(segundo.getTipo() == EnumTipo.flotante):
                return Expresion(EnumTipo.boleano, float(primero.getValor()) <= float(segundo.getValor()))
            else:
                return Expresion(EnumTipo.error, Error(linea, columna, "Semantico", "Menor o igual que no definido entre los tipos " + str(primero.getTipo()) + " y " + str(segundo.getTipo())))
        elif(primero.getTipo() == EnumTipo.cadena):
            if(segundo.getTipo() == EnumTipo.cadena):
                return Expresion(EnumTipo.boleano, str(primero.getValor()) <= str(segundo.getValor()))
            else:
                return Expresion(EnumTipo.error, Error(linea, columna, "Semantico", "Menor o igual que no definido entre los tipos " + str(primero.getTipo()) + " y " + str(segundo.getTipo())))
        else:
            return Expresion(EnumTipo.error, Error(linea, columna, "Semantico", "Menor o igual que no definido entre los tipos " + str(primero.getTipo()) + " y " + str(segundo.getTipo())))

    def operarIgualdad(self, primero, segundo, entorno, linea, columna):
        if(primero.getTipo() == EnumTipo.entero):
            if(segundo.getTipo() == EnumTipo.entero):
                return Expresion(EnumTipo.boleano, int(primero.getValor()) == int(segundo.getValor()))
            elif(segundo.getTipo() == EnumTipo.entero):
                return Expresion(EnumTipo.boleano, float(primero.getValor()) == float(segundo.getValor()))
            else:
                return Expresion(EnumTipo.error, Error(linea, columna, "Semantico", "Igualdad no definida entre los tipos " + str(primero.getTipo()) + " y " + str(segundo.getTipo())))
        elif(primero.getTipo() == EnumTipo.flotante):
            if(segundo.getTipo() == EnumTipo.entero):
                return Expresion(EnumTipo.boleano, float(primero.getValor()) == float(segundo.getValor()))
            elif(segundo.getTipo() == EnumTipo.flotante):
                return Expresion(EnumTipo.boleano, float(primero.getValor()) == float(segundo.getValor()))
            else:
                return Expresion(EnumTipo.error, Error(linea, columna, "Semantico", "Igualdad no definida entre los tipos " + str(primero.getTipo()) + " y " + str(segundo.getTipo())))
        elif(primero.getTipo() == EnumTipo.cadena):
            if(segundo.getTipo() == EnumTipo.cadena):
                return Expresion(EnumTipo.boleano, str(primero.getValor()) == str(segundo.getValor()))
            else:
                return Expresion(EnumTipo.error, Error(linea, columna, "Semantico", "Igualdad no definida entre los tipos " + str(primero.getTipo()) + " y " + str(segundo.getTipo())))
        elif(primero.getTipo() == EnumTipo.boleano):
            if(segundo.getTipo() == EnumTipo.boleano):
                return Expresion(EnumTipo.boleano, bool(primero.getValor()) == bool(segundo.getValor()))
            else:
                return Expresion(EnumTipo.error, Error(linea, columna, "Semantico", "Igualdad no definida entre los tipos " + str(primero.getTipo()) + " y " + str(segundo.getTipo())))
        else:
            return Expresion(EnumTipo.error, Error(linea, columna, "Semantico", "Igualdad no definida entre los tipos " + str(primero.getTipo()) + " y " + str(segundo.getTipo())))

    def operarDiferente(self, primero, segundo, entorno, linea, columna):
        if(primero.getTipo() == EnumTipo.entero):
            if(segundo.getTipo() == EnumTipo.entero):
                return Expresion(EnumTipo.boleano, int(primero.getValor()) != int(segundo.getValor()))
            elif(segundo.getTipo() == EnumTipo.entero):
                return Expresion(EnumTipo.boleano, float(primero.getValor()) != float(segundo.getValor()))
            else:
                return Expresion(EnumTipo.error, Error(linea, columna, "Semantico", "Diferencia no definida entre los tipos " + str(primero.getTipo()) + " y " + str(segundo.getTipo())))
        elif(primero.getTipo() == EnumTipo.flotante):
            if(segundo.getTipo() == EnumTipo.entero):
                return Expresion(EnumTipo.boleano, float(primero.getValor()) != float(segundo.getValor()))
            elif(segundo.getTipo() == EnumTipo.flotante):
                return Expresion(EnumTipo.boleano, float(primero.getValor()) != float(segundo.getValor()))
            else:
                return Expresion(EnumTipo.error, Error(linea, columna, "Semantico", "Diferencia no definida entre los tipos " + str(primero.getTipo()) + " y " + str(segundo.getTipo())))
        elif(primero.getTipo() == EnumTipo.cadena):
            if(segundo.getTipo() == EnumTipo.cadena):
                return Expresion(EnumTipo.boleano, str(primero.getValor()) != str(segundo.getValor()))
            else:
                return Expresion(EnumTipo.error, Error(linea, columna, "Semantico", "Diferencia no definida entre los tipos " + str(primero.getTipo()) + " y " + str(segundo.getTipo())))
        elif(primero.getTipo() == EnumTipo.boleano):
            if(segundo.getTipo() == EnumTipo.boleano):
                return Expresion(EnumTipo.boleano, bool(primero.getValor()) != bool(segundo.getValor()))
            else:
                return Expresion(EnumTipo.error, Error(linea, columna, "Semantico", "Igualdad no definida entre los tipos " + str(primero.getTipo()) + " y " + str(segundo.getTipo())))
        else:
            return Expresion(EnumTipo.error, Error(linea, columna, "Semantico", "Diferencia no definida entre los tipos " + str(primero.getTipo()) + " y " + str(segundo.getTipo())))

    def operarOr(self, primero, segundo, entorno, linea, columna):
        if(primero.getTipo() == EnumTipo.boleano):
            if(segundo.getTipo() == EnumTipo.boleano):
                return Expresion(EnumTipo.boleano, primero.getValor() or segundo.getValor())
            else:
                return Expresion(EnumTipo.error, Error(linea, columna, "Semantico", "Operacion Or no definida entre los tipos " + str(primero.getTipo()) + " y " + str(segundo.getTipo())))
        else:
            return Expresion(EnumTipo.error, Error(linea, columna, "Semantico", "Operacion Or no definida entre los tipos " + str(primero.getTipo()) + " y " + str(segundo.getTipo())))

    def operarAnd(self, primero, segundo, entorno, linea, columna):
        if(primero.getTipo() == EnumTipo.boleano):
            if(segundo.getTipo() == EnumTipo.boleano):
                return Expresion(EnumTipo.boleano, primero.getValor() and segundo.getValor())
            else:
                return Expresion(EnumTipo.error, Error(linea, columna, "Semantico", "Operacion And no definida entre los tipos " + str(primero.getTipo()) + " y " + str(segundo.getTipo())))
        else:
            return Expresion(EnumTipo.error, Error(linea, columna, "Semantico", "Operacion And no definida entre los tipos " + str(primero.getTipo()) + " y " + str(segundo.getTipo())))

    def operarNot(self, primero, entorno, linea, columna):
        if(primero.getTipo() == EnumTipo.boleano):
            return Expresion(EnumTipo.boleano, not primero.getValor())
        else:
            return Expresion(EnumTipo.error, Error(linea, columna, "Semantico", "Operacion Not no definida para el tipo " + str(primero.getTipo())))