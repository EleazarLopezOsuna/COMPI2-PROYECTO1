# Gramatica para primer proyecto 
# Compiladores 2
# Eleazar Jared Lopez Osuna
# 201700893
from Modelos.NodoSintactico import NodoSintactico
import sys
import os
import re
sys.setrecursionlimit(3000)

errores = []
reservadas = {
    'nothing': 'resNothing',
    'Int64':'resInt64',
    'Float64':'resFloat64',
    'Bool':'resBool',
    'Char':'resChar',
    'String':'resString',
    'log10':'reslog10',
    'log':'reslog',
    'sin':'ressin',
    'cos':'rescos',
    'tan':'restan',
    'sqrt':'ressqrt',
    'true':'restrue',
    'false':'resfalse',
    'parse':'resparse',
    'trunc':'restrunc',
    'float':'resfloat',
    'string':'resstring',
    'typeof':'restypeof',
    'pop':'respop',
    'length':'reslength',
    'push':'respush',
    'print':'resprint',
    'println':'resprintln',
    'struct':'resstruct',
    'mutable':'resmutable',
    'end':'resend',
    'uppercase':'resuppercase',
    'lowercase':'reslowercase',
    'global':'resglobal',
    'local':'reslocal',
    'function':'resfunction',
    'if':'resif',
    'elseif':'reselseif',
    'else':'reselse',
    'while':'reswhile',
    'for':'resfor',
    'break':'resbreak',
    'continue':'rescontinue',
    'return':'resreturn',
    'in':'resin'
}

tokens = [
    'DOBLEPUNTOS',
    'DOSPUNTOS',
    'IGUAL',
    'PUNTOCOMA',
    'COMA',
    'SUMA',
    'RESTA',
    'MULTIPLICACION',
    'DIVISION',
    'POTENCIA',
    'MODULO',
    'MAYOR',
    'MENOR',
    'MAYORIGUAL',
    'MENORIGUAL',
    'IGUALIGUAL',
    'DIFERENTE',
    'OR',
    'AND',
    'NOT',
    'PUNTO',
    'CORCHETEA',
    'CORCHETEC'
    'IDENTIFICADOR',
    'ENTERO',
    'FLOTANTE',
    'CADENA',
    'CARACTER'
] + list(reservadas.values())

t_DOBLEPUNTOS       = r'\:\:'
t_DOSPUNTOS         = r'\:'
t_IGUAL             = r'\='
t_PUNTOCOMA         = r'\;'
t_COMA              = r'\,'
t_SUMA              = r'\+'
t_RESTA             = r'\-'
t_MULTIPLICACION    = r'\*'
t_DIVISION          = r'\/'
t_POTENCIA          = r'\^'
t_MODULO            = r'\%'
t_MAYOR             = r'\>'
t_MENOR             = r'\<'
t_MAYORIGUAL        = r'\>\='
t_MENORIGUAL        = r'\<\='
t_IGUALIGUAL        = r'\=\='
t_DIFERENTE         = r'\!\='
t_OR                = r'\|\|'
t_AND               = r'\&\&'
t_NOT               = r'\!'
t_PUNTO             = r'\.'
t_CORCHETEA         = r'\['
t_CORCHETEC         = r'\]'

def t_FLOTANTE(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Float value too large %d", t.value)
        t.value = 0
    return NodoSintactico("FLOTANTE", t.value, t.lineno(1), find_column(input, t.slice[1]))

def t_ENTERO(t):
    r'\d'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return NodoSintactico("ENTERO", t.value, t.lineno(1), find_column(input, t.slice[1]))

def t_IDENTIFICADOR(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reservadas.get(t.value.lower(), 'ID')
    return NodoSintactico("IDENTIFICADOR", t.value, t.lineno(1), find_column(input, t.slice[1]))

def t_CADENA(t):
    r'(\".*?\")'
    t.value = t.value[1:-1]
    return NodoSintactico("CADENA", t.value, t.lineno(1), find_column(input, t.slice[1]))

def t_CARACTER(t):
    r'(\'.\')'
    t.value = t.value[1:-1]
    return NodoSintactico("CARACTER", t.value, t.lineno(1), find_column(input, t.slice[1]))

def t_COMENTARIO_LINEA(t):
    r'\#.*\n'
    t.lexer.lineno += 1

t_ignore = "\t"

def t_new_line(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    errores.append(Exception("Lexico", "Error Lexico: ", t.value[0], t.lexer.lineno, find_column(input, t)))
    t.lexer.skip(1)

def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

import ply.lex as lex
lexer = lex.lex()

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('nonassoc', 'IGUALIGUAL', 'DIFERENTE')
    ('nonassoc', 'MENORQUE', 'MAYORQUE', 'MENORIGUAL', 'MAYORIGUAL'),
    ('left', 'MAS', 'MENOS'),
    ('left', 'DIVISION', 'MULTIPLICACION', 'MODULO'),
    ('left', 'POTENCIA'),
    ('right', 'NOT')
)

def inicio(t):
    'inicio: listaInstrucciones'
    t[0] = NodoSintactico("INICIO", "INICIO", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(t[1])

def listaInstrucciones_1(t):
    'listaInstrucciones: listaInstrucciones instruccion'
    t[1].addHijo(t[2])
    t[0] = t[1]
                
def listaInstrucciones_2(t):
    'listaInstrucciones: instruccion'
    t[0] = NodoSintactico("INSTRUCCION", "INSTRUCCION", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(t[1])

def instruccion_1(t):
    'instruccion: asignacion PUNTOCOMA'
    t[1].addHijo(NodoSintactico("PUNTOCOMA", ";", t.lineno(1), find_column(input, t.slice[1])))
    t[0] = t[1]

def instruccion_2(t):
    'instruccion: asignacionGlobal PUNTOCOMA'
    t[1].addHijo(NodoSintactico("PUNTOCOMA", ";", t.lineno(1), find_column(input, t.slice[1])))
    t[0] = t[1]

def instruccion_3(t):
    'instruccion: asignacionLocal PUNTOCOMA'
    t[1].addHijo(NodoSintactico("PUNTOCOMA", ";", t.lineno(1), find_column(input, t.slice[1])))
    t[0] = t[1]

def instruccion_4(t):
    'instruccion: llamadaFuncion PUNTOCOMA'
    t[1].addHijo(NodoSintactico("PUNTOCOMA", ";", t.lineno(1), find_column(input, t.slice[1])))
    t[0] = t[1]

def instruccion_5(t):
    'instruccion: struct'
    t[0] = t[1]

def instruccion_6(t):
    'instruccion: structMutable'
    t[0] = t[1]

def instruccion_7(t):
    'instruccion: declararFuncion'
    t[0] = t[1]

def instruccion_8(t):
    'instruccion: instruccionIf'
    t[0] = t[1]

def instruccion_9(t):
    'instruccion: instruccionWhile'
    t[0] = t[1]

def instruccion_10(t):
    'instruccion: instruccionFor'
    t[0] = t[1]

def instruccion_11(t):
    'instruccion: resBreak PUNTOCOMA'
    t[0] = NodoSintactico("INSTRUCCIONBREAK", "INSTRUCCIONBREAK", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(NodoSintactico("BREAK", "break", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(NodoSintactico("PUNTOCOMA", ";", t.lineno(1), find_column(input, t.slice[1])))

def instruccion_12(t):
    'instruccion: resContinue PUNTOCOMA'
    t[0] = NodoSintactico("INSTRUCCIONCONTINUE", "INSTRUCCIONCONTINUE", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(NodoSintactico("CONTINUE", "continue", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(NodoSintactico("PUNTOCOMA", ";", t.lineno(1), find_column(input, t.slice[1])))

def instruccion_13(t):
    'instruccion: retorno PUNTOCOMA'
    t[0] = t[1]

def asignacionGlobal(t):
    'asignacionGlobal: resGlobal asignacion'
    t[0] = NodoSintactico("GLOBAL", "GLOBAL", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(NodoSintactico("RESGLOBAL", "global", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(t[2])

def asignacionLocal(t):
    'asignacionLocal: resLocal asignacion'
    t[0] = NodoSintactico("LOCAL", "LOCAL", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(NodoSintactico("RESLOCAL", "local", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(t[2])

def structMutable(t):
    'structMutable: resMutable struct'
    t[0] = NodoSintactico("MUTABLE", "MUTABLE", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(NodoSintactico("RESMUTABLE", "mutable", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(t[2])

def retorno(t):
    'retorno: resReturn expresion'
    t[0] = NodoSintactico("RETORNO", "RETORNO", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(NodoSintactico("RESRETORNO", "return", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(t[2])

def asignacion_1(t):
    'asignacion: IDENTIFICADOR IGUAL expresion DOBLEPUNTOS tipo'
    t[0] = NodoSintactico("ASIGNACION", "ASIGNACION", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(NodoSintactico("IDENTIFICADOR", t[1], t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(NodoSintactico("IGUAL", "=", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(t[3])
    t[0].addHijo(NodoSintactico("DOBLEPUNTOS", "::", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(t[4])

def asignacion_2(t):
    'asignacion: IDENTIFICADOR IGUAL expresion'
    t[0] = NodoSintactico("ASIGNACION", "ASIGNACION", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(NodoSintactico("IDENTIFICADOR", t[1], t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(NodoSintactico("IGUAL", "=", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(t[3])

def asignacion_3(t):
    'asignacion: IDENTIFICADOR accesoFS IGUAL expresion'
    t[0] = NodoSintactico("ASIGNACION", "ASIGNACION", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(NodoSintactico("IDENTIFICADOR", t[1], t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(t[2])
    t[0].addHijo(NodoSintactico("IGUAL", "=", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(t[4])

def asignacion_4(t):
    'asignacion: IDENTIFICADOR dimension IGUAL expresion'
    t[0] = NodoSintactico("ASIGNACION", "ASIGNACION", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(NodoSintactico("IDENTIFICADOR", t[1], t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(t[2])
    t[0].addHijo(NodoSintactico("IGUAL", "=", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(t[4])

def llamadaFuncion_1(t):
    'llamadaFuncion: IDENTIFICADOR PARENTESISA listaExpresiones PARENTESISC'
    t[0] = NodoSintactico("LLAMADAFUNCION", "LLAMADAFUNCION", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(NodoSintactico("IDENTIFICADOR", t[1], t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(NodoSintactico("PARENTESISA", "(", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(t[3])
    t[0].addHijo(NodoSintactico("PARENTESISC", ")", t.lineno(1), find_column(input, t.slice[1])))

def llamadaFuncion_2(t):
    'llamadaFuncion: IDENTIFICADOR PARENTESISA PARENTESISC'
    t[0] = NodoSintactico("LLAMADAFUNCION", "LLAMADAFUNCION", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(NodoSintactico("IDENTIFICADOR", t[1], t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(NodoSintactico("PARENTESISA", "(", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(NodoSintactico("PARENTESISC", ")", t.lineno(1), find_column(input, t.slice[1])))

def llamadaFuncion_3(t):
    'llamadaFuncion: resPush PARENTESISA expresion PARENTESISC'
    t[0] = NodoSintactico("LLAMADAFUNCION", "LLAMADAFUNCION", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(NodoSintactico("PUSH", "push", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(NodoSintactico("PARENTESISA", "(", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(t[3])
    t[0].addHijo(NodoSintactico("PARENTESISC", ")", t.lineno(1), find_column(input, t.slice[1])))

def llamadaFuncion_4(t):
    'llamadaFuncion: resPrint PARENTESISA listaExpresiones PARENTESISC'
    t[0] = NodoSintactico("LLAMADAFUNCION", "LLAMADAFUNCION", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(NodoSintactico("PRINT", "print", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(NodoSintactico("PARENTESISA", "(", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(t[3])
    t[0].addHijo(NodoSintactico("PARENTESISC", ")", t.lineno(1), find_column(input, t.slice[1])))

def llamadaFuncion_5(t):
    'llamadaFuncion: resPrintln PARENTESISA listaExpresiones PARENTESISC'
    t[0] = NodoSintactico("LLAMADAFUNCION", "LLAMADAFUNCION", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(NodoSintactico("PRINTLN", "println", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(NodoSintactico("PARENTESISA", "(", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(t[3])
    t[0].addHijo(NodoSintactico("PARENTESISC", ")", t.lineno(1), find_column(input, t.slice[1])))

def struct(t):
    'struct: resStruct IDENTIFICADOR bloqueStruct resEnd PUNTOCOMA'
    t[0] = NodoSintactico("NOMUTABLESTRUCT", "NOMUTABLESTRUCT", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(NodoSintactico("STRUCT", "struct", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(NodoSintactico("IDENTIFICADOR", t[2], t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(t[3])
    t[0].addHijo(NodoSintactico("END", "end", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(NodoSintactico("PUNTOCOMA", ";", t.lineno(1), find_column(input, t.slice[1])))

def declararFuncion_1(t):
    'declararFuncion: resFunction IDENTIFICADOR PARENTESISA listaParametros PARENTESISC listaInstrucciones resEnd PUNTOCOMA'
    t[0] = NodoSintactico("DECLARARFUNCION", "DECLARARFUNCION", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(NodoSintactico("FUNCTION", "function", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(NodoSintactico("IDENTIFICADOR", t[2], t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(NodoSintactico("PARENTESISA", "(", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(t[4])
    t[0].addHijo(NodoSintactico("PARENTESISC", ")", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(t[6])
    t[0].addHijo(NodoSintactico("END", "end", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(NodoSintactico("PUNTOCOMA", ";", t.lineno(1), find_column(input, t.slice[1])))

def declararFuncion_2(t):
    'declararFuncion: resFuncion IDENTIFICADOR PARENTESISA PARENTESISC listaInstrucciones resEnd PUNTOCOMA'
    t[0] = NodoSintactico("DECLARARFUNCION", "DECLARARFUNCION", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(NodoSintactico("FUNCTION", "function", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(NodoSintactico("IDENTIFICADOR", t[2], t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(NodoSintactico("PARENTESISA", "(", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(NodoSintactico("PARENTESISC", ")", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(t[5])
    t[0].addHijo(NodoSintactico("END", "end", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(NodoSintactico("PUNTOCOMA", ";", t.lineno(1), find_column(input, t.slice[1])))

def instruccionIf_1(t):
    'instruccionIf: resIf expresion listaInstrucciones resEnd PUNTOCOMA'
    t[0] = NodoSintactico("BLOQUEIF", "BLOQUEIF", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(NodoSintactico("IF", "if", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(t[2])
    t[0].addHijo(t[3])
    t[0].addHijo(NodoSintactico("END", "end", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(NodoSintactico("PUNTOCOMA", ";", t.lineno(1), find_column(input, t.slice[1])))

def instruccionIf_2(t):
    'instruccionIf: resIf expresion listaInstrucciones resElse listaInstrucciones resEnd PUNTOCOMA'
    t[0] = NodoSintactico("BLOQUEIF", "BLOQUEIF", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(NodoSintactico("IF", "if", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(t[2])
    t[0].addHijo(t[3])
    t[0].addHijo(NodoSintactico("ELSE", "else", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(t[5])
    t[0].addHijo(NodoSintactico("END", "end", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(NodoSintactico("PUNTOCOMA", ";", t.lineno(1), find_column(input, t.slice[1])))

def instruccionIf_3(t):
    'instruccionIf: resIf expresion listaInstrucciones condicionElseif resElse listaIntrucciones resEnd PUNTOCOMA'
    t[0] = NodoSintactico("BLOQUEIF", "BLOQUEIF", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(NodoSintactico("IF", "if", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(t[2])
    t[0].addHijo(t[3])
    t[4].addHijo(NodoSintactico("ELSE", "else", t.lineno(1), find_column(input, t.slice[1])))
    t[4].addHijo(t[6])
    t[4].addHijo(NodoSintactico("END", "end", t.lineno(1), find_column(input, t.slice[1])))
    t[4].addHijo(NodoSintactico("PUNTOCOMA", ";", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(t[4])

def instruccionElseif_1(t):
    'instruccionElseif: instruccionElseif resElseif expresion listaInstrucciones'
    nuevo = NodoSintactico("ELSEIF", "elseif", t.lineno(1), find_column(input, t.slice[1]))
    nuevo.addHijo(t[3])
    nuevo.addHijo(t[4])
    t[1].addHijo(nuevo)
    t[0] = t[1]

def instruccionElseif_2(t):
    'instruccionElseif: resElseif expresion listaInstrucciones'
    t[0] = NodoSintactico("ELSEIF", "elseif", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(t[1])
    t[0].addHijo(t[2])

def instruccionWhile(t):
    'instruccionWhile: resWhile expresion listaInstrucciones resEnd PUNTOCOMA'
    t[0] = NodoSintactico("WHILE", "while", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(t[2])
    t[0].addHijo(t[3])
    t[0].addHijo(NodoSintactico("END", "end", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(NodoSintactico("PUNTOCOMA", ";", t.lineno(1), find_column(input, t.slice[1])))

def instruccionFor(t):
    'resFor IDENTIFICADOR resIn expresion listaInstrucciones resEnd PUNTOCOMA'
    t[0] = NodoSintactico("FOR", "for", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(t[1])
    t[0].addHijo(NodoSintactico("IN", "in", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(t[3])
    t[0].addHijo(t[4])
    t[0].addHijo(NodoSintactico("END", "end", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(NodoSintactico("PUNTOCOMA", ";", t.lineno(1), find_column(input, t.slice[1])))

def expresion_1(t):
    'expresion: aritmetica'
    t[0] = NodoSintactico("EXPRESION", "EXPRESION", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(t[1])

def expresion_2(t):
    'expresion: relacionales'
    t[0] = NodoSintactico("EXPRESION", "EXPRESION", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(t[1])

def expresion_3(t):
    'expresion: logicas'
    t[0] = NodoSintactico("EXPRESION", "EXPRESION", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(t[1])

def expresion_4(t):
    'expresion: nativa'
    t[0] = NodoSintactico("EXPRESION", "EXPRESION", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(t[1])

def expresion_5(t):
    'expresion: resTrue'
    t[0] = NodoSintactico("EXPRESION", "EXPRESION", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(NodoSintactico("TRUE", "true", t.lineno(1), find_column(input, t.slice[1])))

def expresion_6(t):
    'expresion: resFalse'
    t[0] = NodoSintactico("EXPRESION", "EXPRESION", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(NodoSintactico("FALSE", "false", t.lineno(1), find_column(input, t.slice[1])))

def expresion_7(t):
    'expresion: IDENTIFICADOR'
    t[0] = NodoSintactico("EXPRESION", "EXPRESION", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(t[1])

def expresion_8(t):
    'expresion: ENTERO'
    t[0] = NodoSintactico("EXPRESION", "EXPRESION", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(t[1])

def expresion_9(t):
    'expresion: CADENA'
    t[0] = NodoSintactico("EXPRESION", "EXPRESION", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(t[1])

def expresion_10(t):
    'expresion: CARACTER'
    t[0] = NodoSintactico("EXPRESION", "EXPRESION", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(t[1])

def expresion_11(t):
    'expresion: FLOTANTE'
    t[0] = NodoSintactico("EXPRESION", "EXPRESION", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(t[1])

def expresion_14(t):
    'expresion: llamadaFuncion'
    t[0] = NodoSintactico("EXPRESION", "EXPRESION", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(t[1])

def expresion_15(t):
    'expresion: CORCHETEA listaExpresiones CORCHETEC'
    t[0] = NodoSintactico("EXPRESION", "EXPRESION", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(NodoSintactico("CORCHETEA", "[", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(t[2])
    t[0].addHijo(NodoSintactico("CORCHETEC", "]", t.lineno(1), find_column(input, t.slice[1])))

def expresion_16(t):
    'expresion: IDENTIFICADOR accesoFS'
    t[0] = NodoSintactico("EXPRESION", "EXPRESION", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(t[1])
    t[0].addHijo(t[2])

def expresion_17(t):
    'expresion: llamadaFuncion accesoFS'
    t[0] = NodoSintactico("EXPRESION", "EXPRESION", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(t[1])
    t[0].addHijo(t[2])

def expresion_18(t):
    'expresion: construccionStruct'
    t[0] = NodoSintactico("EXPRESION", "EXPRESION", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(t[1])

def expresion_19(t):
    'expresion: PARENTESISA expresion PARENTESISC'
    t[0] = NodoSintactico("EXPRESION", "EXPRESION", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(NodoSintactico("PARENTESISA", "(", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(t[2])
    t[0].addHijo(NodoSintactico("PARENTESISC", ")", t.lineno(1), find_column(input, t.slice[1])))

def expresion_20(t):
    'expresion: expresion DOSPUNTOS expresion'
    t[0] = NodoSintactico("EXPRESION", "EXPRESION", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(t[1])
    t[0].addHijo(NodoSintactico("DOSPUNTOS", ":", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(t[3])

def expresion_21(t):
    'expresion: IDENTIFICADOR dimension'
    t[0] = NodoSintactico("EXPRESION", "EXPRESION", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(t[1])
    t[0].addHijo(t[2])

def tipo_1(t):
    'tipo: resNothing'
    t[0] = NodoSintactico("EXPRESION", "EXPRESION", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(NodoSintactico("NOTHING", "nothing", t.lineno(1), find_column(input, t.slice[1])))

def tipo_2(t):
    'tipo: resInt64'
    t[0] = NodoSintactico("EXPRESION", "EXPRESION", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(NodoSintactico("INT64", "int64", t.lineno(1), find_column(input, t.slice[1])))

def tipo_3(t):
    'tipo: resFloat64'
    t[0] = NodoSintactico("EXPRESION", "EXPRESION", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(NodoSintactico("FLOAT64", "float64", t.lineno(1), find_column(input, t.slice[1])))

def tipo_4(t):
    'tipo: resBool'
    t[0] = NodoSintactico("EXPRESION", "EXPRESION", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(NodoSintactico("NOTHING", "nothing", t.lineno(1), find_column(input, t.slice[1])))

def tipo_5(t):
    'tipo: resChar'
    t[0] = NodoSintactico("EXPRESION", "EXPRESION", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(NodoSintactico("CHAR", "char", t.lineno(1), find_column(input, t.slice[1])))

def tipo_6(t):
    'tipo: resString'
    t[0] = NodoSintactico("EXPRESION", "EXPRESION", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(NodoSintactico("STRING", "string", t.lineno(1), find_column(input, t.slice[1])))

def tipo_7(t):
    'tipo: IDENTIFICADOR'
    t[0] = NodoSintactico("EXPRESION", "EXPRESION", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(t[1])

def accesoFS_1(t):
    'accesoFS: accesoFS PUNTO IDENTIFICADOR'
    t[1].addHijo(NodoSintactico("PUNTO", ".", t.lineno(1), find_column(input, t.slice[1])))
    t[1].addHijo(t[3])
    t[0] = t[1]

def accesoFS_2(t):
    'accesoFS: PUNTO IDENTIFICADOR'
    t[0] = NodoSintactico("ACCESOFS", "accesofs", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(NodoSintactico("PUNTO", ".", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(t[2])

def listaParametros_1(t):
    'listaParametros: COMA listaParametros IDENTIFICADOR'
    t[2].addHijo(NodoSintactico("COMA", ",", t.lineno(1), find_column(input, t.slice[1])))
    t[2].addHijo(t[3])
    t[0] = t[2]

def listaParametros_2(t):
    'listaParametros: COMA listaParametros IDENTIFICADOR DOBLEPUNTOS tipo'
    t[2].addHijo(NodoSintactico("COMA", ",", t.lineno(1), find_column(input, t.slice[1])))
    t[2].addHijo(t[3])
    t[2].addHijo(NodoSintactico("DOBLEPUNTOS", "::", t.lineno(1), find_column(input, t.slice[1])))
    t[2].addHijo(t[5])
    t[0] = t[2]

def listaParametros_3(t):
    'listaParametros: IDENTIFICADOR DOBLEPUNTOS tipo'
    t[0] = NodoSintactico("LISTAPARAMETROS", "LISTAPARAMETROS", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(t[1])
    t[0].addHijo(NodoSintactico("DOBLEPUNTOS", "::", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(t[3])

def listaParametros_4(t):
    'listaParametros: IDENTIFICADOR'
    t[0] = NodoSintactico("LISTAPARAMETROS", "LISTAPARAMETROS", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(t[1])

def bloqueStruct(t):
    'bloqueStruct: bloqueStruct asignacion'
    t[1].addHijo(t[2])
    t[0] = t[1]

def bloqueStruct_2(t):
    'bloqueStruct: asignacion'
    t[0] = NodoSintactico("BLOQUESTRUCT", "BLOQUESTRUCT", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(t[1])

def dimension_1(t):
    'dimension: dimension CORCHETEA expresion CORCHETEC'
    t[1].addHijo(NodoSintactico("CORCHETEA", "[", t.lineno(1), find_column(input, t.slice[1])))
    t[1].addHijo(t[3])
    t[1].addHijo(NodoSintactico("CORCHETEC", "]", t.lineno(1), find_column(input, t.slice[1])))

def dimension_2(t):
    'dimension: CORCHETEA expresion CORCHETEC'
    t[0].addHijo(NodoSintactico("DIMENSION", "DIMENSION", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(NodoSintactico("CORCHETEA", "[", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(t[2])
    t[0].addHijo(NodoSintactico("CORCHETEC", "]", t.lineno(1), find_column(input, t.slice[1])))

def construccionStruct(t):
    'construccionStruct: IDENTIFICADOR PARENTESISA listaAsignaciones PARENTESISC'
    t[0] = NodoSintactico("CONSTRUCCIONSTRUCT", "CONSTRUCCIONSTRUCT", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(t[1])
    t[0].addHijo(NodoSintactico("PARENTESISA", "(", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(t[3])
    t[0].addHijo(NodoSintactico("PARENTESISC", ")", t.lineno(1), find_column(input, t.slice[1])))

def listaAsignaciones(t):
    'listaAsignaciones: COMA listaAsignaciones asignacion'
    t[2].addHijo(NodoSintactico("COMA", ",", t.lineno(1), find_column(input, t.slice[1])))
    t[2].addHijo(t[3])
    t[0] = t[2]

def listaAsignaciones_2(t):
    'listaAsignaciones: asignacion'
    t[0] = NodoSintactico("LISTAASIGNACIONES", "LISTAASIGNACIONES", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(t[1])

def aritmetica_1(t):
    'aritmetica: expresion SUMA expresion'
    t[0] = NodoSintactico("SUMA", "SUMA", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(t[1])
    t[0].addHijo(NodoSintactico("MAS", "+", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(t[3])

def aritmetica_2(t):
    'aritmetica: expresion RESTA expresion'
    t[0] = NodoSintactico("RESTA", "RESTA", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(t[1])
    t[0].addHijo(NodoSintactico("MENOS", "-", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(t[3])

def aritmetica_3(t):
    'aritmetica: expresion MULTIPLICACION expresion'
    t[0] = NodoSintactico("MULTIPLICACION", "MULTIPLICACION", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(t[1])
    t[0].addHijo(NodoSintactico("ASTERISCO", "*", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(t[3])

def aritmetica_4(t):
    'aritmetica: expresion DIVISION expresion'
    t[0] = NodoSintactico("DIVISION", "DIVISION", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(t[1])
    t[0].addHijo(NodoSintactico("SLASH", "/", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(t[3])

def aritmetica_5(t):
    'aritmetica: expresion POTENCIA expresion'
    t[0] = NodoSintactico("POTENCIA", "POTENCIA", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(t[1])
    t[0].addHijo(NodoSintactico("ACENTO", "^", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(t[3])

def aritmetica_6(t):
    'aritmetica: expresion MODULO expresion'
    t[0] = NodoSintactico("MODULO", "MODULO", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(t[1])
    t[0].addHijo(NodoSintactico("PORCENTAJE", "%", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(t[3])

def aritmetica_7(t):
    'aritmetica: RESTA expresion'
    t[0] = NodoSintactico("NEGATIVO", "NEGATIVO", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(NodoSintactico("MENOS", "-", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(t[2])

def nativa_1(t):
    'nativa: resLog10 PARENTESISA expresion PARENTESISC'
    t[0] = NodoSintactico("LOGNATURAL", "LOGNATURAL", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(NodoSintactico("LOG10", "log10", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(NodoSintactico("PARENTESISA", "(", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(t[3])
    t[0].addHijo(NodoSintactico("PARENTESISC", ")", t.lineno(1), find_column(input, t.slice[1])))

def nativa_2(t):
    'nativa: resLog PARENTESISA expresion COMA expresion PARENTESISC'
    t[0] = NodoSintactico("LOGBASE", "LOGBASE", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(NodoSintactico("LOG", "log", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(NodoSintactico("PARENTESISA", "(", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(t[3])
    t[0].addHijo(NodoSintactico("COMA", ",", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(t[5])
    t[0].addHijo(NodoSintactico("PARENTESISC", ")", t.lineno(1), find_column(input, t.slice[1])))

def nativa_3(t):
    'nativa: resSeno PARENTESISA expresion PARENTESISC'
    t[0] = NodoSintactico("SENO", "SENO", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(NodoSintactico("SIN", "sin", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(NodoSintactico("PARENTESISA", "(", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(t[3])
    t[0].addHijo(NodoSintactico("PARENTESISC", ")", t.lineno(1), find_column(input, t.slice[1])))

def nativa_4(t):
    'nativa: resCoseno PARENTESISA expresion PARENTESISC'
    t[0] = NodoSintactico("COSENO", "COSENO", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(NodoSintactico("COS", "cos", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(NodoSintactico("PARENTESISA", "(", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(t[3])
    t[0].addHijo(NodoSintactico("PARENTESISC", ")", t.lineno(1), find_column(input, t.slice[1])))

def nativa_5(t):
    'nativa: resTangente PARENTESISA expresion PARENTESISC'
    t[0] = NodoSintactico("TANGENTE", "TANGENTE", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(NodoSintactico("TAN", "tan", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(NodoSintactico("PARENTESISA", "(", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(t[3])
    t[0].addHijo(NodoSintactico("PARENTESISC", ")", t.lineno(1), find_column(input, t.slice[1])))

def nativa_6(t):
    'nativa: resRaiz PARENTESISA expresion PARENTESISC'
    t[0] = NodoSintactico("RAIZ", "RAIZ", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(NodoSintactico("SQRT", "sqrt", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(NodoSintactico("PARENTESISA", "(", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(t[3])
    t[0].addHijo(NodoSintactico("PARENTESISC", ")", t.lineno(1), find_column(input, t.slice[1])))

def nativa_7(t):
    'nativa: resParse PARENTESISA resInt64 COMA expresion PARENTESISC'
    t[0] = NodoSintactico("PARSEINT", "PARSEINT", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(NodoSintactico("PARSE", "parse", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(NodoSintactico("PARENTESISA", "(", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(NodoSintactico("INT64", "int64", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(NodoSintactico("COMA", ",", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(t[5])
    t[0].addHijo(NodoSintactico("PARENTESISC", ")", t.lineno(1), find_column(input, t.slice[1])))

def nativa_8(t):
    'nativa: resParse PARENTESISA resFloat64 COMA expresion PARENTESISC'
    t[0] = NodoSintactico("PARSEFLOAT", "PARSEFLOAT", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(NodoSintactico("PARSE", "parse", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(NodoSintactico("PARENTESISA", "(", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(NodoSintactico("FLOAT64", "float64", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(NodoSintactico("COMA", ",", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(t[5])
    t[0].addHijo(NodoSintactico("PARENTESISC", ")", t.lineno(1), find_column(input, t.slice[1])))

def nativa_9(t):
    'nativa: resTrunc PARENTESISA expresion PARENTESISC'
    t[0] = NodoSintactico("TRUNCAR", "TRUNCAR", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(NodoSintactico("TRUNC", "trunc", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(NodoSintactico("PARENTESISA", "(", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(t[3])
    t[0].addHijo(NodoSintactico("PARENTESISC", ")", t.lineno(1), find_column(input, t.slice[1])))

def nativa_10(t):
    'nativa: resFloat PARENTESISA expresion PARENTESISC'
    t[0] = NodoSintactico("CONVERTIRFLOAT", "CONVERTIRFLOAT", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(NodoSintactico("FLOAT64", "float64", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(NodoSintactico("PARENTESISA", "(", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(t[3])
    t[0].addHijo(NodoSintactico("PARENTESISC", ")", t.lineno(1), find_column(input, t.slice[1])))

def nativa_11(t):
    'nativa: resStringFunc PARENTESISA expresion PARENTESISC '
    t[0] = NodoSintactico("CONVERTIRSTRING", "CONVERTIRSTRING", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(NodoSintactico("STRING", "string", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(NodoSintactico("PARENTESISA", "(", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(t[3])
    t[0].addHijo(NodoSintactico("PARENTESISC", ")", t.lineno(1), find_column(input, t.slice[1])))

def nativa_12(t):
    'nativa: resTypeof PARENTESISA expresion PARENTESISC'
    t[0] = NodoSintactico("OBTENERTIPO", "OBTENERTIPO", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(NodoSintactico("TYPEOF", "typeof", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(NodoSintactico("PARENTESISA", "(", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(t[3])
    t[0].addHijo(NodoSintactico("PARENTESISC", ")", t.lineno(1), find_column(input, t.slice[1])))

def nativa_13(t):
    'nativa: resPop PARENTESISA IDENTIFICADOR PARENTESISC'
    t[0] = NodoSintactico("HACERPOP", "HACERPOP", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(NodoSintactico("POP", "pop", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(NodoSintactico("PARENTESISA", "(", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(t[3])
    t[0].addHijo(NodoSintactico("PARENTESISC", ")", t.lineno(1), find_column(input, t.slice[1])))

def nativa_14(t):
    'nativa: resLength PARENTESISA IDENTIFICADOR PARENTESISC'
    t[0] = NodoSintactico("OBTENERSIZE", "OBTENERSIZE", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(NodoSintactico("LENGTH", "length", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(NodoSintactico("PARENTESISA", "(", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(t[3])
    t[0].addHijo(NodoSintactico("PARENTESISC", ")", t.lineno(1), find_column(input, t.slice[1])))

def nativa_15(t):
    'nativa: resUppercase PARENTESISA expresion PARENTESISC'
    t[0] = NodoSintactico("HACERUPPERCASE", "HACERUPPERCASE", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(NodoSintactico("UPPERCASE", "uppercase", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(NodoSintactico("PARENTESISA", "(", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(t[3])
    t[0].addHijo(NodoSintactico("PARENTESISC", ")", t.lineno(1), find_column(input, t.slice[1])))

def nativa_16(t):
    'nativa: resLowercase PARENTESISA expresion PARENTESISC'
    t[0] = NodoSintactico("HACERLOWERCASE", "HACERLOWERCASE", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(NodoSintactico("LOWERCASE", "lowercase", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(NodoSintactico("PARENTESISA", "(", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(t[3])
    t[0].addHijo(NodoSintactico("PARENTESISC", ")", t.lineno(1), find_column(input, t.slice[1])))

def relacionales_1(t):
    'relacionales: expresion MAYOR expresion'
    t[0] = NodoSintactico("MAYOR", "MAYOR", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(t[1])
    t[0].addHijo(NodoSintactico("MAYORQUE", ">", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(t[3])

def relacionales_2(t):
    'relacionales: expresion MENOR expresion'
    t[0] = NodoSintactico("MENOR", "MENOR", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(t[1])
    t[0].addHijo(NodoSintactico("MENORQUE", "<", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(t[3])

def relacionales_3(t):
    'relacionales: expresion MAYORIGUAL expresion'
    t[0] = NodoSintactico("MAYORIGUAL", "MAYORIGUAL", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(t[1])
    t[0].addHijo(NodoSintactico("MAYORIGUALQUE", ">=", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(t[3])

def relacionales_4(t):
    'relacionales: expresion MENORIGUAL expresion'
    t[0] = NodoSintactico("MENORIGUAL", "MENORIGUAL", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(t[1])
    t[0].addHijo(NodoSintactico("MENORIGUALQUE", "<=", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(t[3])

def relacionales_5(t):
    'relacionales: expresion IGUALIGUAL expresion'
    t[0] = NodoSintactico("IGUALDAD", "IGUALDAD", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(t[1])
    t[0].addHijo(NodoSintactico("IGUALQUE", "==", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(t[3])

def relacionales_6(t):
    'relacionales: expresion DIFERENTE expresion'
    t[0] = NodoSintactico("DIFERENCIA", "DIFERENCIA", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(t[1])
    t[0].addHijo(NodoSintactico("DIFERENTEA", "!=", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(t[3])

def logicas_1(t):
    'logicas: expresion OR expresion'
    t[0] = NodoSintactico("OR", "OR", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(t[1])
    t[0].addHijo(NodoSintactico("BARRAS", "||", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(t[3])

def logicas_2(t):
    'logicas: expresion AND expresion'
    t[0] = NodoSintactico("AND", "AND", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(t[1])
    t[0].addHijo(NodoSintactico("AMPERSON", "&&", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(t[3])

def logicas_3(t):
    'logicas: NOT expresion'
    t[0] = NodoSintactico("NOT", "NOT", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(NodoSintactico("NEGACION", "!", t.lineno(1), find_column(input, t.slice[1])))
    t[0].addHijo(t[2])

def listaExpresiones_1(t):
    'listaExpresiones: COMA listaExpresiones expresion'
    t[2].addHijo(NodoSintactico("COMA", ",", t.lineno(1), find_column(input, t.slice[1])))
    t[2].addHijo(t[3])
    t[0] = t[2]

def listaExpresiones_2(t):
    'listaExpresiones: expresion'
    t[0] = NodoSintactico("LISTAEXPRESIONES", "LISTAEXPRESIONES", t.lineno(1), find_column(input, t.slice[1]))
    t[0].addHijo(t[1])

import ply.yacc as yacc
parser = yacc.yacc()

def getErrores():
    return errores

def parse(inp):
    global errores
    global lexer
    global parser
    errores = []
    lexer = lex.lex(reflags = re.IGNORECASE)
    parser = yacc.yacc()
    global input
    input = inp
    instrucciones = parser.parse(inp)
    return 0