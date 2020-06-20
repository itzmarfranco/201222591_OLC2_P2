from graphviz import Graph
from graphviz import nohtml
import re

import os

from graphviz import Digraph
import pydotplus

from node import Node
from SymbolTable import Table, Symbol
from Error import Error, ErrorList

import math


def analize(entrada):
    
    reserved = {
        'auto': 'AUTO',
        'break': 'BREAK',
        'case': 'CASE',
        'char': 'CHAR',
        'const': 'CONST',
        'continue': 'CONTINUE',
        'default': 'DEFAULT',
        'do': 'DO',
        'double': 'DOUBLE',
        'else': 'ELSE',
        'enum': 'AUTO',
        'extern': 'EXTERN',
        'float': 'FLOAT',
        'for': 'FOR',
        'goto': 'GOTO',
        'if': 'IF',
        'int': 'INT',
        'printf': 'PRINTF',
        'register': 'REGISTER',
        'return': 'RETURN',
        'scanf': 'SCANF',
        'sizeof': 'SIZEOF',
        'struct': 'STRUCT',
        'switch': 'SWITCH',
        'void': 'VOID',
        'while': 'WHILE',
    }
    # Create a list to hold all of the token names
    tokens = [
        'COLON', # :
        'QUESTION', # ?
        'COMMA', # ,
        'DOT', # .
        'SEMICOLON', # ;
        'L_PAR', # (
        'R_PAR', # )
        'ASSIGN', # =
        'COMMENT', # //comment
        'COMMENT_MULTI', # /*....*/
        'NAME', # id

        'PLUS', # +
        'MINUS', # -
        'UMINUS', # - unario
        'MULTIPLY', # *
        'DIVIDE', # /
        'REMAINDER', # %

        'APLUS', # +=
        'AMINUS', # -=
        'AMULTIPLY', # *=
        'ADIVIDE', # /=
        'AREMAINDER', # %=
        'ASHIFT_R', # <<=
        'ASHIFT_L', # >>=
        'AAND', # &=
        'AOR', # |=
        'AXOR', # ^=

        'PLUSPLUS', # ++
        'MINUSMINUS', # --

        'EQUAL', # ==
        'NOT_EQUAL', # !=
        'GREATER', # >
        'LESS', # <
        'GREATER_EQUAL', # >=
        'LESS_EQUAL', # <=


        'NOT', # !
        'AND', # &&
        'OR', # ||

        'AND_B', # &
        'OR_B', # |
        'NOT_B', # ~
        'XOR_B', # ^
        'SHIFT_L', # <<
        'SHIFT_R', # >>
        
        'L_BRACKET', # [
        'R_BRACKET', # ]
        'QUOTE_1', # '
        'QUOTE_2', # "

        'INTEGER', # 1 2 3...
        'DECIMAL', # 1.54...
        'STRING', # hello
        'CHARACTER' # p 

    ] + list(reserved.values())

    # Use regular expressions to define what each token is
    COLON = r'\:' # :
    QUESTION = r'\?' # ?
    COMMA = r'\,' # 
    DOT = r'\.' # .
    SEMICOLON = r'\;' # ;
    L_PAR = r'\(' # (
    R_PAR = r'\)' # )
    ASSIGN = r'\=' # =
    #COMMENT = r'\/\/' # //comment
    #NAME = r'\c' # id
    PLUS = r'\+' # +
    MINUS = r'\-' # -
    UMINUS = r'\-' # - unario
    MULTIPLY = r'\*' # *
    DIVIDE = r'\/' # /
    REMAINDER = r'\%' # %
    APLUS = r'\+\=' # +=
    AMINUS = r'\-\=' # -=
    AMULTIPLY = r'\*\=' # *=
    ADIVIDE = r'\/\=' # /=
    AREMAINDER = r'\%\=' # %=
    ASHIFT_R = r'\>\>\=' # >>=
    ASHIFT_L = r'\<\<\=' # <<=
    AAND = r'\&\=' # &=
    AOR = r'\|\=' # |=
    AXOR = r'\^\=' # ^=
    PLUSPLUS = r'\+\+' # ++
    MINUSMINUS = r'\-\-' # --
    EQUAL = r'\=\=' # ==
    NOT_EQUAL = r'\!\=' # !=
    GREATER = r'\>' # >
    LESS = r'\<' # <
    GREATER_EQUAL = r'\>\=' # >=
    LESS_EQUAL = r'\<\=' # <=
    NOT = r'\!' # !
    AND = r'\&\&' # &&
    OR = r'\|\|' # ||
    AND_B = r'\&' # &
    OR_B = r'\|' # |
    NOT_B = r'\~' # ~
    XOR_B = r'\^' # ^
    SHIFT_L = r'\<\<' # <<
    SHIFT_R = r'\>\>' # >>
    L_BRACKET = r'\[' # [
    R_BRACKET = r'\]' # ]
    QUOTE_1 = r'\"' # 
    QUOTE_2 = r'\'' # "
    #INTEGER = r'\c' # 1 2 3...
    #DECIMAL = r'\c' # 1.54...
    #STRING = r'\c' # hello
    #CHARACTER = r'\c' # p 

    # Ply's special t_ignore variable allows us to define characters the lexer will ignore.
    # We're ignoring spaces.
    t_ignore = ' \t'

    # More complicated tokens, such as tokens that are more than 1 character in length
    # are defined using functions.
    # A float is 1 or more numbers followed by a dot (.) followed by 1 or more numbers again.
    
    def t_DECIMAL(t):
        r'\d+\.\d+'
        t.value = float(t.value)
        return t

    # An int is 1 or more numbers.
    def t_INTEGER(t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_STRING(t):
        r'(\' | \").*?(\' | \")'
        t.value = t.value[1:-1]
        return t 

    def t_COMMENT_MULTI(t):
        r'/\*(.|\n)*?\*/'
        t.lexer.lineno += t.value.count('\n')

    def t_COMMENT(t):
        r'//.*\n'
        t.lexer.lineno += 1

    # A NAME is a variable name. A variable can be 1 or more characters in length.
    # The first character must be in the ranges a-z A-Z or be an underscore.
    # Any character following the first character can be a-z A-Z 0-9 or an underscore.
    def t_NAME(t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        #r'\?'
        #t.type = 'NAME'
        t.type = reserved.get(t.value, 'NAME')
        return t

    def t_newLine(t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")

    def find_column(input, token):
        line_start = input.rfind('\n', 0, token.lexpos) + 1
        return (token.lexpos - line_start) + 1
        
    # Skip the current token and output 'Illegal characters' using the special Ply t_error function.
    def t_error(t):
        #print("Illegal characters!")
        t.lexer.skip(1)
        error = Error('Caracter no permitido: '+ str(t.value), t.lineno,0)
        lexicalErrors.add(error)

    # Build the lexer
    log = []
    from .ply import lex as lex
    lexer = lex.lex()

    # Ensure our parser understands the correct order of operations.
    # The precedence variable is a special Ply variable.
    precedence = (
        ('left', 'OR_B'),
        ('left', 'AND_B'),
        ('left', 'OR'),
        ('left', 'AND'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'MULTIPLY', 'DIVIDE'),
        ('right', 'UMINUS')
    )


    # Define our grammar. We allow expressions, var_assign's and empty's.
    def p_start(p):
        '''
        '''
        p[0] = ()

    #Empty production
    def p_empty(p):
        '''
        empty :
        '''
        p[0] = None
        log.append('<tr><td>empty : </td><td>p[0] = None</td><td>'+ str(p.lineno(0)) +'</td><td>Produccion vacia</td></tr>')


    def p_error(p):
        if p:
            #print("Syntax error at token", p.type)
            # Just discard the token and tell the parser it's okay.
            parser.errok()
        else:
            #print("Syntax error at EOF")
            pass
        #print(t)
        #print("Error sintactico: " + str(t.value) + " , tipo: " + str(t.type))
        #print("Linea: " + str(t.lineno) + " ,Columna: " + str(t.lexpos))
        error = Error('Error en el token '+ str(p.type), str(p.lineno), 0)
        syntacticErrors.add(error)

    
    ts = Table([])

    lexicalErrors = ErrorList([])
    syntacticErrors = ErrorList([])
    semanticErrors = ErrorList([])
    #  lineal AST
    tree = None

    counter = 0
    def graphAST(tree):
        if type(tree) == tuple:
            for node in tree:
                print(node)
                graphAST(node)
        else:
            print('n'+str(counter), ' [label = '+ node[0] +']')
 
    def runTag(tree1, tree2):
        if type(tree1) == tuple:
            size = len(tree1)
            for i in range(0, size):
                if type(tree1[i]) == tuple:
                    try:
                        runTag(tree1[i], tree1[i+1])
                    except:
                        runTag(tree1[i], None)
                else:
                    if tree1[i] == 'tag':
                        #print('ETIQUETA ENCONTRADA', tree1[1], '->', tree2)
                        sym = Symbol(tree1[1], 'tag', None, None, tree2)
                        ts.add(sym)

    # flag to know if label encountered, 1=yes. If yes, 
    flag = 0

    def run(tree):
        if type(tree) == tuple:
            for node in tree:
                if type(node) == tuple:
                    if node[0] == 'goto':
                        if ts.isSymbolInTable(node[1]):
                            sym = ts.get(node[1])
                            return run(sym.tree)
                        else:
                            error = Error('No se ha declarado la etiqueta \''+ str(node[1])+'\'', 0,0)
                            semanticErrors.add(error)
                        break
                    elif node[0] == 'if':
                        if run(node[1]) == True:
                            if ts.isSymbolInTable(node[2]):
                                sym = ts.get(node[2])
                                return run(sym.tree)
                            else:
                                error = Error('No se ha declarado la etiqueta \''+ str(node[2])+'\'', 0,0)
                                semanticErrors.add(error)
                            break
                        else:
                            #NOT TRUE
                            pass
                    else:
                        run(node)
                else:
                    if node == '=':
                        if tree[1] == 'array_a':
                            if ts.isSymbolInTable(tree[2]) and ts.get(tree[2]).length == 2:
                                if run(tree[4]) != None:
                                    #print('ASSIGNING ARRAY ', tree[2],'[',run(tree[3]), '] -> ', run(tree[4]))
                                    #p[0] = ('=', 'array_a', p[1], p[3], p[6])
                                    varType = ''
                                    if isinstance(run(tree[4]), str):
                                        varType = 'str'
                                    elif isinstance(run(tree[4]), int):
                                        varType = 'int'
                                    elif isinstance(run(tree[4]), float):
                                        varType = 'flt'

                                    id = str(tree[2]) + '[' + str(run(tree[3])) + ']'
                                    sym = Symbol(id, varType, run(tree[4]), 1, ())
                                    ts.add(sym)
                                    return
                                else:
                                    error = Error('No se puede asignar valor \'None\'', 0,0)
                                    semanticErrors.add(error)
                                    return
                            else:
                                error = Error('Arreglo \''+str(tree[2])+'\' no declarado', 0,0)
                                semanticErrors.add(error)
                        elif tree[1] == 'abs':
                            if isinstance(run(tree[3]), int) or isinstance(run(tree[3]), float):
                                # calculate abs(tree[3])
                                absValue = abs(run(tree[3]))
                                varType = ''
                                if isinstance(run(tree[3]), int):
                                    varType = 'int'
                                else:
                                    varType = 'flt'
                                # store tree[2] in ts
                                sym = Symbol(tree[2], varType , absValue, 1, ())
                                ts.add(sym)
                            else:
                                pass
                        else:
                            if run(tree[2]) != None:
                                #print('ASSIGNING ', tree[1], ' -> ', run(tree[2]))
                                varType = ''
                                if isinstance(run(tree[2]), str):
                                    varType = 'str'
                                elif isinstance(run(tree[2]), int):
                                    varType = 'int'
                                elif isinstance(run(tree[2]), float):
                                    varType = 'flt'

                                sym = Symbol(tree[1], varType, run(tree[2]), 1, ())
                                ts.add(sym)
                                return
                            else:
                                error = Error('No se puede asignar valor \'None\'', 0,0)
                                semanticErrors.add(error)
                                return
                        #store in symbol table
                    elif node == '+':
                        if run(tree[1]) == None or run(tree[2]) == None:
                            error = Error('No se puede operar con \'+\' valor  \'None\'', 0,0)
                            semanticErrors.add(error)
                            return
                        elif isinstance(run(tree[2]), str) and (isinstance(run(tree[1]), int) or isinstance(run(tree[1]), float)):
                            error = Error('No se puede sumar cadena y número', 0,0)
                            semanticErrors.add(error)
                            return
                        elif isinstance(run(tree[1]), str) and (isinstance(run(tree[2]), int) or isinstance(run(tree[2]), float)):
                            error = Error('No se puede sumar cadena y número', 0,0)
                            semanticErrors.add(error)
                            return
                        else:
                            return run(tree[1]) + run(tree[2])
                    elif node == '-':
                        if len(tree) == 3:
                            if run(tree[1]) == None or run(tree[2]) == None:
                                error = Error('No se puede operar con \'-\' valor  \'None\'', 0,0)
                                semanticErrors.add(error)
                                return
                            elif isinstance(run(tree[1]), str) or isinstance(run(tree[2]), str):
                                error = Error('No se puede restar cadena y número', 0,0)
                                semanticErrors.add(error)
                                return
                            else:
                                return run(tree[1]) - run(tree[2])
                        else:
                            if run(tree[1]) == None:
                                error = Error('No se puede operar con \'-\' valor  \'None\'', 0,0)
                                semanticErrors.add(error)
                                return
                            elif isinstance(run(tree[1]), str):
                                error = Error('No se puede restar cadena y número', 0,0)
                                semanticErrors.add(error)
                                return
                            else:
                                return -run(tree[1])
                    elif node == '*':
                        if run(tree[1]) == None or run(tree[2]) == None:
                            error = Error('No se puede operar con \'*\' valor  \'None\'', 0,0)
                            semanticErrors.add(error)
                            return
                        elif isinstance(run(tree[1]), str) or isinstance(run(tree[2]), str):
                            error = Error('No se puede multiplicar cadena', 0,0)
                            semanticErrors.add(error)
                            return
                        else:
                            return run(tree[1]) * run(tree[2])
                    elif node == '/':
                        if run(tree[1]) == None or run(tree[2]) == None:
                            error = Error('No se puede operar con \'*\' valoor \'None\'', 0,0)
                            semanticErrors.add(error)
                            return
                        elif isinstance(run(tree[1]), str) or isinstance(run(tree[2]), str):
                            error = Error('No se puede dividir cadena y número', 0,0)
                            semanticErrors.add(error)
                            return
                        elif run(tree[2]) == 0:
                            error = Error('No se puede dividir entre 0', 0,0)
                            semanticErrors.add(error)
                            return
                        else:
                            return run(tree[1]) / run(tree[2])
                    elif node == '%':
                        if run(tree[1]) == None or run(tree[2]) == None:
                            error = Error('No se puede operar con \'/\' valor  \'None\'', 0,0)
                            semanticErrors.add(error)
                            return
                        if isinstance(run(tree[1]), str) or isinstance(run(tree[2]), str):
                            error = Error('No se puede dividir cadena y número', 0,0)
                            semanticErrors.add(error)
                            return
                        elif run(tree[2]) == 0:
                            error = Error('No se puede obtener residuo de división entre 0', 0,0)
                            semanticErrors.add(error)
                            return
                        else:
                            return run(tree[1]) % run(tree[2])
                    elif node == 'if':
                        print('IF',  run(tree[1]), tree[2])
                        #call 'search' function to locate tag and execute from there
                    elif node == '<':
                        if run(tree[1]) == None or run(tree[2]) == None:
                            error = Error('No se puede comparar con \'<\' valor \'None\'', 0,0)
                            semanticErrors.add(error)
                            return
                        elif isinstance(run(tree[1]), str) and (isinstance(run(tree[2]), int) or isinstance(run(tree[2]), float)):
                            error = Error('No se puede comparar con \'<\' cadena y número', 0,0)
                            semanticErrors.add(error)
                            return
                        elif isinstance(run(tree[2]), str) and (isinstance(run(tree[1]), int) or isinstance(run(tree[1]), float)):
                            error = Error('No se puede comparar \'<\' cadena y número', 0,0)
                            semanticErrors.add(error)
                            return
                        else:
                            return run(tree[1]) < run(tree[2])
                    elif node == '>':
                        if run(tree[1]) == None or run(tree[2]) == None:
                            error = Error('No se puede comparar con \'>\' valor \'None\'', 0,0)
                            semanticErrors.add(error)
                            return
                        elif isinstance(run(tree[1]), str) and (isinstance(run(tree[2]), int) or isinstance(run(tree[2]), float)):
                            error = Error('No se puede comparar con \'>\' cadena y número', 0,0)
                            semanticErrors.add(error)
                            return
                        elif isinstance(run(tree[2]), str) and (isinstance(run(tree[1]), int) or isinstance(run(tree[1]), float)):
                            error = Error('No se puede comparar con \'>\' cadena y número', 0,0)
                            semanticErrors.add(error)
                            return
                        else:
                            return run(tree[1]) > run(tree[2])
                    elif node == '<=':
                        if run(tree[1]) == None or run(tree[2]) == None:
                            error = Error('No se puede comparar con \'<=\' valor \'None\'', 0,0)
                            semanticErrors.add(error)
                            return
                        elif isinstance(run(tree[1]), str) and (isinstance(run(tree[2]), int) or isinstance(run(tree[2]), float)):
                            error = Error('No se puede comparar con \'<=\' cadena y número', 0,0)
                            semanticErrors.add(error)
                            return
                        elif isinstance(run(tree[2]), str) and (isinstance(run(tree[1]), int) or isinstance(run(tree[1]), float)):
                            error = Error('No se puede comparar con \'<=\' cadena y número', 0,0)
                            semanticErrors.add(error)
                            return
                        else:
                            return run(tree[1]) <= run(tree[2])
                    elif node == '>=':
                        if run(tree[1]) == None or run(tree[2]) == None:
                            error = Error('No se puede comparar con \'>=\' valor \'None\'', 0,0)
                            semanticErrors.add(error)
                            return
                        elif isinstance(run(tree[1]), str) and (isinstance(run(tree[2]), int) or isinstance(run(tree[2]), float)):
                            error = Error('No se puede comparar con \'>=\' cadena y número', 0,0)
                            semanticErrors.add(error)
                            return
                        elif isinstance(run(tree[2]), str) and (isinstance(run(tree[1]), int) or isinstance(run(tree[1]), float)):
                            error = Error('No se puede comparar con \'>=\' cadena y número', 0,0)
                            semanticErrors.add(error)
                            return
                        else:
                            return run(tree[1]) >= run(tree[2])
                    elif node == '==':
                        if run(tree[1]) == None or run(tree[2]) == None:
                            error = Error('No se puede comparar con \'==\' valor \'None\'', 0,0)
                            semanticErrors.add(error)
                            return
                        elif isinstance(run(tree[1]), str) and (isinstance(run(tree[2]), int) or isinstance(run(tree[2]), float)):
                            error = Error('No se puede comparar con \'==\' cadena y número', 0,0)
                            semanticErrors.add(error)
                            return
                        elif isinstance(run(tree[2]), str) and (isinstance(run(tree[1]), int) or isinstance(run(tree[1]), float)):
                            error = Error('No se puede comparar con \'==\' cadena y número', 0,0)
                            semanticErrors.add(error)
                            return
                        else:
                            return run(tree[1]) == run(tree[2])
                    elif node == '!=':
                        if run(tree[1]) == None or run(tree[2]) == None:
                            error = Error('No se puede comparar con \'!=\' valor \'None\'', 0,0)
                            semanticErrors.add(error)
                            return
                        elif isinstance(run(tree[1]), str) and (isinstance(run(tree[2]), int) or isinstance(run(tree[2]), float)):
                            error = Error('No se puede comparar con \'!=\' cadena y número', 0,0)
                            semanticErrors.add(error)
                            return
                        elif isinstance(run(tree[2]), str) and (isinstance(run(tree[1]), int) or isinstance(run(tree[1]), float)):
                            error = Error('No se puede comparar con \'!=\' cadena y número', 0,0)
                            semanticErrors.add(error)
                            return
                        else:
                            return run(tree[1]) != run(tree[2])
                    elif node == '&&':
                        if run(tree[1]) == None or run(tree[2]) == None:
                            error = Error('No se puede comparar con \'&&\' valor \'None\'', 0,0)
                            semanticErrors.add(error)
                            return
                        elif run(tree[1]) not in (0,1) or run(tree[2]) not in (0,1):
                            error = Error('No se puede comparar con \'&&\' valores no booleanos', 0,0)
                            semanticErrors.add(error)
                            return
                        else:
                            return run(tree[1]) and run(tree[2])
                    elif node == '||':
                        if run(tree[1]) == None or run(tree[2]) == None:
                            error = Error('No se puede comparar con \'||\' valor \'None\'', 0,0)
                            semanticErrors.add(error)
                            return
                        elif run(tree[1]) not in (0,1) or run(tree[2]) not in (0,1):
                            error = Error('No se puede comparar con \'||\' valores no booleanos', 0,0)
                            semanticErrors.add(error)
                            return
                        else:
                            return run(tree[1]) or run(tree[2])
                    elif node == '!':
                        if run(tree[1]) == None or run(tree[2]) == None:
                            error = Error('No se puede comparar con \'<\' valor \'None\'', 0,0)
                            semanticErrors.add(error)
                            return
                        elif run(tree[1]) not in (0,1):
                            error = Error('No se puede comparar con \'!\' valores no booleanos', 0,0)
                            semanticErrors.add(error)
                            return
                        else:
                            return not run(tree[1])
                    elif node == 'xor':
                        if run(tree[1]) == None or run(tree[2]) == None:
                            error = Error('No se puede comparar con \'xor\' valor \'None\'', 0,0)
                            semanticErrors.add(error)
                            return
                        elif run(tree[1]) not in (0,1) or run(tree[2]) not in (0,1):
                            error = Error('No se puede comparar con \'xor\' valores no booleanos', 0,0)
                            semanticErrors.add(error)
                            return
                        else:
                            return run(tree[1]) != run(tree[2])
                    elif node == '&':
                        if run(tree[1]) == None or run(tree[2]) == None:
                            error = Error('No se puede comparar con \'&\' valor \'None\'', 0,0)
                            semanticErrors.add(error)
                            return
                        elif isinstance(run(tree[1]), str) or isinstance(run(tree[2]), str) or isinstance(run(tree[1]), float) or isinstance(run(tree[2]), float):
                            error = Error('No se puede comparar con \'&\' cadena o decimal', 0,0)
                            semanticErrors.add(error)
                            return
                        else:
                            return run(tree[1]) & run(tree[2])
                    elif node == '|':
                        if run(tree[1]) == None or run(tree[2]) == None:
                            error = Error('No se puede comparar con \'|\' valor \'None\'', 0,0)
                            semanticErrors.add(error)
                            return
                        elif isinstance(run(tree[1]), str) or isinstance(run(tree[2]), str) or isinstance(run(tree[1]), float) or isinstance(run(tree[2]), float):
                            error = Error('No se puede comparar con \'|\' cadena o decimal', 0,0)
                            semanticErrors.add(error)
                            return
                        else:
                            return run(tree[1]) | run(tree[2])
                    elif node == '~':
                        if run(tree[1]) == None:
                            error = Error('No se puede operar con \'~\' valor \'None\'', 0,0)
                            semanticErrors.add(error)
                            return
                        elif isinstance(run(tree[1]), str) or isinstance(run(tree[1]), float):
                            error = Error('Cannot operate \'~\' cadena o decimal', 0,0)
                            semanticErrors.add(error)
                            return
                        else:
                            return ~(run(tree[1]))
                    elif node == '^':
                        if run(tree[1]) == None or run(tree[2]) == None:
                            error = Error('No se puede operar con \'^\' valor \'None\'', 0,0)
                            semanticErrors.add(error)
                            return
                        elif isinstance(run(tree[1]), str) or isinstance(run(tree[2]), str) or isinstance(run(tree[1]), float) or isinstance(run(tree[2]), float):
                            error = Error('No se puede operar con \'^\' cadena o decimal', 0,0)
                            semanticErrors.add(error)
                            return
                        else:
                            return run(tree[1]) ^ run(tree[2])
                    elif node == '<<':
                        if run(tree[1]) == None or run(tree[2]) == None:
                            error = Error('No se puede usar valor \'None\' al desplazar', 0,0)
                            semanticErrors.add(error)
                            return
                        elif isinstance(run(tree[1]), str) or isinstance(run(tree[2]), str) or isinstance(run(tree[1]), float) or isinstance(run(tree[2]), float):
                            error = Error('No se puede usar \'<<\' con cadena o decimal', 0,0)
                            semanticErrors.add(error)
                            if run(tree[2]) < 0:
                                error = Error('No se puede desplazar pasos negativos', 0,0)
                                semanticErrors.add(error)
                                return
                        else:
                            return run(tree[1]) << run(tree[2])
                    elif node == '>>':
                        if run(tree[1]) == None or run(tree[2]) == None:
                            error = Error('No se puede usar valor \'None\' al desplazar', 0,0)
                            semanticErrors.add(error)
                            return
                        if isinstance(run(tree[1]), str) or isinstance(run(tree[2]), str) or isinstance(run(tree[1]), float) or isinstance(run(tree[2]), float):
                            error = Error('No se puede usar \'>>\' con cadena o decimal', 0,0)
                            semanticErrors.add(error)
                            if run(tree[2]) < 0:
                                error = Error('No se puede desplazar pasos negativos', 0,0)
                                semanticErrors.add(error)
                                return
                            else:
                                return run(tree[1]) >> run(tree[2])
                    elif node == 'print':
                        # buscar en tabla de simbolos el valor de run(tree[1])
                        return print(run(tree[1]))
                    elif node == 'print_array':
                        # buscar en tabla de simbolos el valor de run(tree[1])
                        return print(run(tree[1]))
                    elif node == 'unset':
                        # buscar en la tabla de símbolos la variable, eliminar el registro
                        if ts.isSymbolInTable(tree[1]):
                            ts.remove(tree[1])
                        else:
                            error = Error('No se ha declarado la variable \''+ str(tree[1])+'\'', 0,0)
                            semanticErrors.add(error)
                    elif node == 'exit':
                        # fin de la ejecución
                        #return print('EXITING')
                        break
                    elif node == 'convert':
                        if tree[1] == 'int':
                            # get value from TS
                            var = tree[2]
                            if ts.isSymbolInTable(tree[2]):
                                sym = ts.get(tree[2])
                                if sym.varType == 'flt':
                                    return math.floor(sym.value)
                                elif sym.varType == 'str':
                                    return ord(sym.value[0])
                                elif sym.varType == 'array':
                                    # get all values for array
                                    array = []
                                    #(index,value,type)
                                    for s in ts.symbols:
                                        if len(s.id.split('[')) > 1:
                                            id = s.id.split('[')[0]
                                            index = s.id.split('[')[1].split(']')[0]
                                            if id == var and s.value != None:
                                                array.append((index, s.value, s.varType))
                                    array.sort()
                                    if array[0][2] == 'int':
                                        return array[0][1]
                                    elif array[0][2] == 'flt':
                                        return math.floor(array[0][1])
                                    elif array[0][2] == 'str':
                                        return ord(array[0][1][0])
                                elif sym.varType == 'int':
                                    return sym.value
                            else:
                                pass
                        elif tree[1] == 'float':
                            # get value from TS
                            var = tree[2]
                            if ts.isSymbolInTable(tree[2]):
                                sym = ts.get(tree[2])
                                if sym.varType == 'flt':
                                    return sym.value
                                elif sym.varType == 'str':
                                    return ord(math.floor(sym.value[0]))
                                elif sym.varType == 'array':
                                    # get all values for array
                                    array = []
                                    #(index,value,type)
                                    for s in ts.symbols:
                                        if len(s.id.split('[')) > 1:
                                            id = s.id.split('[')[0]
                                            index = s.id.split('[')[1].split(']')[0]
                                            if id == var and s.value != None:
                                                array.append((index, s.value, s.varType))
                                    array.sort()
                                    if array[0][2] == 'int':
                                        return float(array[0][1])
                                    elif array[0][2] == 'flt':
                                        return array[0][1]
                                    elif array[0][2] == 'str':
                                        return ord(math.floor(array[0][1][0]))
                                elif sym.varType == 'int':
                                    return float(sym.value)
                            else:
                                pass
                        elif tree[1] == 'char':
                            # get value from TS
                            var = tree[2]
                            if ts.isSymbolInTable(tree[2]):
                                sym = ts.get(tree[2])
                                if sym.varType == 'flt':
                                    newVal = math.floor(sym.value)
                                    if newVal < 256:
                                        return chr(newVal)
                                    elif sym.value >= 256:
                                        return chr(newVal % 256)
                                    else:
                                        error = Error('No se puede convertir a caracter un número negativo', 0,0)
                                        semanticErrors.add(error)
                                        return 
                                elif sym.varType == 'str':
                                    return sym.value[0]
                                elif sym.varType == 'array':
                                    # get all values for array
                                    array = []
                                    #(index,value,type)
                                    for s in ts.symbols:
                                        if len(s.id.split('[')) > 1:
                                            id = s.id.split('[')[0]
                                            index = s.id.split('[')[1].split(']')[0]
                                            if id == var and s.value != None:
                                                array.append((index, s.value, s.varType))
                                    array.sort()
                                    if array[0][2] == 'int':
                                        newVal = array[0][1]
                                        if newVal < 256:
                                            return chr(newVal)
                                        elif newVal >= 256:
                                            return chr(newVal % 256)
                                        else:
                                            error = Error('No se puede convertir a caracter un número negativo', 0,0)
                                            semanticErrors.add(error)
                                            return
                                    elif array[0][2] == 'flt':
                                        newVal = array[0][1]
                                        if newVal < 256:
                                            return chr(newVal)
                                        elif sym.value >= 256:
                                            return chr(newVal % 256)
                                        else:
                                            error = Error('No se puede convertir a caracter un número negativo', 0,0)
                                            semanticErrors.add(error)
                                            return 
                                    elif array[0][2] == 'str':
                                        return array[0][1][0]
                                elif sym.varType == 'int':
                                    if sym.value < 256:
                                        return chr(sym.value)
                                    elif sym.value >= 256:
                                        return chr(sym.value % 256)
                                    else:
                                        error = Error('No se puede convertir a caracter un número negativo', 0,0)
                                        semanticErrors.add(error)
                                        return
                            else:
                                pass
                    elif node == 'goto':
                        # search for label in ts, then run the the asociated to the label
                        # if ts.isSymbolInTable(tree[1]):
                        #     flag = 1
                        #     sym = ts.get(tree[1])
                        #     return run(sym.tree)
                        # else:
                        #     error = Error('No se ha declarado la etiqueta \''+ str(tree[1])+'\'', 0,0)
                        #     semanticErrors.add(error)
                        return print('JUMPING TO', tree[1])
                    elif node == 'tag':
                        # labels were previously stored in ts
                        return #print('ADDING TAG', tree[1])
                    elif node == 'array':
                        # guardar variable como arreglo en la tabla de simbolos
                        sym = Symbol(tree[1], 'array', None, 2, ())
                        ts.add(sym)
                        #return print('CREATING ARRAY', tree[1])                                        
                    elif node == 'read':
                        # capturar entrada escrita en la terminal
                        # guardar en la tabla de simbolos
                        var = input('>>')
                        varType = ''
                        try:
                            varInt = int(var)
                            varType = 'int'
                        except:
                                try:
                                    varFloat = float(var)
                                    varType = 'flt'
                                except:
                                    varType = 'str'

                        id = str(tree[1])
                        sym = Symbol(id, varType, var, 1, ())
                        ts.add(sym)
                        return #print('READING TO', tree[1])
                    else:
                        pass
        else:
            if isinstance(tree, str):
                if tree[0] == '$':
                    # seach in TS
                    if ts.isSymbolInTable(tree):
                        #print('return value', ts.get(tree).value)
                        return ts.get(tree).value
                    else:
                        errorStr = 'Variable \''+ str(tree) + '\' No definida'
                        error = Error(errorStr, 0,0)
                        semanticErrors.add(error)
                        return None
                else:
                    # Will return string
                    return tree
            else:
                # will return number
                return tree



    from .ply import yacc as yacc
    parser = yacc.yacc()

    
    ast = parser.parse(entrada,tracking=True)


    dotDataReport = 'digraph{tbl[shape=plaintext\nlabel=<<table><tr><td colspan=\'4\'>Reporte gramatical</td></tr>'
    dotDataReport = dotDataReport + '<tr><td>Produccion</td><td>Acciones</td><td>Línea</td><td>Descripción</td></tr>'
    for x in reversed(log):
        dotDataReport = dotDataReport + x
    dotDataReport = dotDataReport + '</table>>];}'

    reportGraph = pydotplus.graph_from_dot_data(dotDataReport)
    reportGraph.write_pdf('Reporte_gramatical.pdf')

    dotDataTS = 'digraph{tbl[shape=plaintext\nlabel=<<table><tr><td colspan=\'4\'>Tabla de símbolos</td></tr>'
    #dotDataTS = dotDataTS + '<tr><td>ID</td><td>Tipo</td><td>Valor</td><td>Longitud</td><td>Arbol asociado</td></tr>'
    dotDataTS = dotDataTS + '<tr><td>ID</td><td>Tipo</td><td>Valor</td><td>Longitud</td></tr>'
    for sym in ts.symbols:
        #dotDataTS += '<tr><td>'+str(sym.id)+'</td><td>'+str(sym.varType)+'</td><td>'+str(sym.value)+'</td><td>'+str(sym.length)+'</td><td>'+str(sym.tree)+'</td></tr>'
        dotDataTS += '<tr><td>'+str(sym.id)+'</td><td>'+str(sym.varType)+'</td><td>'+str(sym.value)+'</td><td>'+str(sym.length)+'</td></tr>'
    dotDataTS = dotDataTS + '</table>>];}'

    tsGraph = pydotplus.graph_from_dot_data(dotDataTS)
    tsGraph.write_pdf('Reporte_TablaSimbolos.pdf')

    dotDataErrors = 'digraph{tbl[shape=plaintext\nlabel=<<table><tr><td colspan=\'3\'>Reporte de errores</td></tr>'
    dotDataErrors = dotDataErrors + '<tr><td>Error</td><td>Tipo</td><td>Linea</td></tr>'
    for e in lexicalErrors.errors:
        dotDataErrors += '<tr><td>'+str(e.value)+'</td><td>Léxico</td><td>'+str(e.line)+'</td></tr>'

    for e in syntacticErrors.errors:
        dotDataErrors += '<tr><td>'+str(e.value)+'</td><td>Sintáctico</td><td>'+str(e.line)+'</td></tr>'

    for e in semanticErrors.errors:
        dotDataErrors += '<tr><td>'+str(e.value)+'</td><td>Semántico</td><td>'+str(e.line)+'</td></tr>'

    dotDataErrors = dotDataErrors + '</table>>];}'

    errorGraph = pydotplus.graph_from_dot_data(dotDataErrors)
    errorGraph.write_pdf('Reporte_Errores.pdf')



    return ast