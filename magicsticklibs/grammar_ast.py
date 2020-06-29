from graphviz import Graph
import re

from graphviz import nohtml

import os

from graphviz import Digraph
import pydotplus

i = 0
def inc():
    global i
    i = i+1
    return i


def analizeAST(entrada):

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
        'enum': 'ENUM',
        'extern': 'EXTERN',
        'float': 'FLOAT',
        'for': 'FOR',
        'goto': 'GOTO',
        'if': 'IF',
        'int': 'INT',
        #'main': 'MAIN',
        'printf': 'PRINTF',
        'register': 'REGISTER',
        'return': 'RETURN',
        'scanf': 'SCANF',
        'signed': 'SIGNED',
        'sizeof': 'SIZEOF',
        'static': 'STATIC',
        'struct': 'STRUCT',
        'typedef': 'TYPEDEF',
        'switch': 'SWITCH',
        'union': 'UNION',
        'unsigned': 'UNSIGNED',
        'void': 'VOID',
        'volatile': 'VOLATILE',
        'while': 'WHILE'
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
        'L_CURLY', # {
        'R_CURLY', # }
        'ASSIGN', # =
        'ACCESS', # ->
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
    t_COLON = r'\:' # :
    t_QUESTION = r'\?' # ?
    t_COMMA = r'\,' # 
    t_DOT = r'\.' # .
    t_SEMICOLON = r'\;' # ;
    t_L_PAR = r'\(' # (
    t_R_PAR = r'\)' # )
    t_L_CURLY = r'\{'
    t_R_CURLY = r'\}'
    t_ASSIGN = r'\=' # =
    t_ACCESS = r'\-\>' # ->
    #COMMENT = r'\/\/' # //comment
    #NAME = r'\c' # id
    t_PLUS = r'\+' # +
    t_MINUS = r'\-' # -
    t_UMINUS = r'\-' # - unario
    t_MULTIPLY = r'\*' # *
    t_DIVIDE = r'\/' # /
    t_REMAINDER = r'\%' # %
    t_APLUS = r'\+\=' # +=
    t_AMINUS = r'\-\=' # -=
    t_AMULTIPLY = r'\*\=' # *=
    t_ADIVIDE = r'\/\=' # /=
    t_AREMAINDER = r'\%\=' # %=
    t_ASHIFT_R = r'\>\>\=' # >>=
    t_ASHIFT_L = r'\<\<\=' # <<=
    t_AAND = r'\&\=' # &=
    t_AOR = r'\|\=' # |=
    t_AXOR = r'\^\=' # ^=
    t_PLUSPLUS = r'\+\+' # ++
    t_MINUSMINUS = r'\-\-' # --
    t_EQUAL = r'\=\=' # ==
    t_NOT_EQUAL = r'\!\=' # !=
    t_GREATER = r'\>' # >
    t_LESS = r'\<' # <
    t_GREATER_EQUAL = r'\>\=' # >=
    t_LESS_EQUAL = r'\<\=' # <=
    t_NOT = r'\!' # !
    t_AND = r'\&\&' # &&
    t_OR = r'\|\|' # ||
    t_AND_B = r'\&' # &
    t_OR_B = r'\|' # |
    t_NOT_B = r'\~' # ~
    t_XOR_B = r'\^' # ^
    t_SHIFT_L = r'\<\<' # <<
    t_SHIFT_R = r'\>\>' # >>
    t_L_BRACKET = r'\[' # [
    t_R_BRACKET = r'\]' # ]
    t_QUOTE_1 = r'\"' # 
    t_QUOTE_2 = r'\'' # "
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
        # An int is 1 or more numbers.
    def t_INTEGER(t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_DECIMAL(t):
        r'\d+\.\d+'
        t.value = float(t.value)
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
        #error = Error('Caracter no permitido: '+ str(t.value[0]), t.lineno,0)
        #lexicalErrors.add(error)

    # Build the lexer
    log = []
    from .ply import lex as lex
    lexer = lex.lex()

    # Ensure our parser understands the correct order of operations.
    # The precedence variable is a special Ply variable.
    # precedence = (
    #     ('left', 'OR_B'),
    #     ('left', 'AND_B'),
    #     ('left', 'OR'),
    #     ('left', 'AND'),
    #     ('left', 'PLUS', 'MINUS'),
    #     ('left', 'MULTIPLY', 'DIVIDE'),
    #     ('right', 'UMINUS')
    # )

    #dot = Digraph(comment='AST')
    dot = Graph(name='AST')
    dot.attr(splines='false', rankdir="TBLR")
    dot.node_attr.update(shape= 'rect')
    dot.edge_attr.update(color= 'red', arrowhead = 'normal', arrowtail ="dot")
    # Define our grammar. We allow expressions, var_assign's and empty's.
    def p_Decls_1(p):
        '''
        Decls : Decl Decls
        '''
        #print('AST')
        id = inc()
        p[0] = id
        dot.node(str(id), 'DECLS')
        dot.edge(str(id), str(p[1]))
        dot.edge(str(id), str(p[2]))

    def p_Decls_2(p):
        '''
        Decls : empty
        '''
        p[0] = None

    def p_Decl(p):
        '''
        Decl : Func_Decl
            | Func_Proto
            | Struct_Decl
            | Union_Decl
            | Enum_Decl
            | Var_Decl    
            | Typedef_Decl
        '''
        id = inc()
        p[0] = id
        dot.node(str(id), 'DECL')
        dot.edge(str(id), str(p[1]))

    # ===================================================================
    # Function  Declaration
    # ===================================================================

    def p_Func_Proto(p):
        '''
        Func_Proto : Func_ID L_PAR Types  R_PAR SEMICOLON
            | Func_ID L_PAR Params R_PAR SEMICOLON
            | Func_ID L_PAR R_PAR SEMICOLON
        '''

    def p_Func_Decl_1(p):
        '''
        Func_Decl : Func_ID L_PAR Params  R_PAR Block
        '''
        id = inc()
        p[0] = id
        dot.node(str(id), 'FUNC_DECL')
        dot.edge(str(id), str(p[1]))
        dot.edge(str(id), str(p[3]))
        dot.edge(str(id), str(p[5]))

    def p_Func_Decl_2(p):
        '''
        Func_Decl : Func_ID L_PAR Id_List R_PAR Struct_Def Block
        '''
        id = inc()
        p[0] = id
        dot.node(str(id), 'FUNC_DECL')
        dot.edge(str(id), str(p[1]))
        dot.edge(str(id), str(p[2]))
        dot.edge(str(id), str(p[5]))
        dot.edge(str(id), str(p[6]))

    def p_Func_Decl_3(p):
        '''
        Func_Decl : Func_ID L_PAR R_PAR Block
        '''
        id = inc()
        p[0] = id
        dot.node(str(id), 'FUNC_DECL')
        dot.edge(str(id), str(p[1]))
        dot.edge(str(id), str(p[4]))

    def p_Params_1(p):
        '''
        Params : Param COMMA Params
        '''
        id = inc()
        p[0] = id
        dot.node(str(id), 'PARAMS')
        dot.edge(str(id), str(p[1]))
        dot.edge(str(id), str(p[3]))

    def p_Params_2(p):
        '''
        Params : Param
        '''
        id = inc()
        p[0] = id
        dot.node(str(id), 'PARAMS')
        dot.edge(str(id), str(p[1]))

    def p_Param_1(p):
        '''
        Param : CONST Type NAME
        '''
        id = inc()
        p[0] = id
        dot.node(str(id), 'PARAM')
        dot.edge(str(id), 'const')
        dot.edge(str(id), str(p[2]))
        dot.edge(str(id), str(p[3]))

    def p_Param_2(p):
        '''
        Param : Type NAME
        '''
        id = inc()
        p[0] = id
        dot.node(str(id), 'PARAM')
        dot.edge(str(id), str(p[1]))
        dot.edge(str(id), str(p[2]))

    def p_Types_1(p):
        '''
        Types : Type COMMA Types
        '''
        id = inc()
        p[0] = id
        dot.node(str(id), 'TYPES')
        dot.edge(str(id), str(p[1]))
        dot.edge(str(id), str(p[3]))

    def p_Types_2(p):
        '''
        Types : Type 
        '''
        id = inc()
        p[0] = id
        dot.node(str(id), 'TYPES')
        dot.edge(str(id), str(p[1]))

    def p_Id_List_1(p):
        '''
        Id_List : NAME COMMA Id_List
        '''
        id = inc()
        p[0] = id
        dot.node(str(id), 'ID_LIST')
        id = inc()
        dot.node(str(id), str(p[1]))
        dot.edge(str(id-1), str(p[3]))

    def p_Id_List_2(p):
        '''
        Id_List : NAME
        '''
        id = inc()
        p[0] = id
        dot.node(str(id), 'ID_LIST')
        dot.edge(str(id), str(p[1]))

    def p_Func_ID_1(p):
        '''
        Func_ID : Type NAME
        '''
        id = inc()
        p[0] = id
        dot.node(str(id), 'FUNC_ID')
        dot.edge(str(id), str(p[1]))
        dot.edge(str(id), str(p[2]))

    def p_Func_ID_2(p):
        '''
        Func_ID : NAME
        '''
        id = inc()
        p[0] = id
        dot.node(str(id), 'FUNC_ID')
        dot.edge(str(id), str(p[1]))

    # ===================================================================
    # Type Declaration
    # ===================================================================

    def p_Typedef_Decl(p):
        '''
        Typedef_Decl : TYPEDEF Type NAME SEMICOLON
        '''
        p[0] = ('typedef', p[2], p[3])

    def p_Struct_Decl(p):
        '''
        Struct_Decl  : STRUCT NAME L_CURLY Struct_Def R_CURLY  SEMICOLON 
        '''
        id = inc()
        p[0] = id
        dot.node(str(id), 'STRUCT_DECL')
        id = inc()
        dot.node(str(id), 'struct')
        dot.edge(str(p[0]), str(id))
        dot.edge(str(p[0]), str(p[2]))
        dot.edge(str(p[0]), str(p[4]))

    def p_Union_Decl(p):
        '''
        Union_Decl : UNION NAME L_CURLY Struct_Def R_CURLY  SEMICOLON 
        '''
        id = inc()
        p[0] = id
        dot.node(str(id), 'UNION_DECL')
        dot.edge(str(id), 'union')
        dot.edge(str(id), str(p[2]))
        dot.edge(str(id), str(p[4]))

    def p_Struct_Def_1(p):
        '''
        Struct_Def : Var_Decl Struct_Def
        '''
        id = inc()
        p[0] = id
        dot.node(str(id), 'STRUCT_DEF')
        dot.edge(str(id), str(p[1]))
        dot.edge(str(id), str(p[2]))

    def p_Struct_Dec2(p):
        '''
        Struct_Def : Var_Decl
        '''
        id = inc()
        p[0] = id
        dot.node(str(id), 'STRUCT_DEF')
        dot.edge(str(id), str(p[1]))

    # ===================================================================
    # Variable Declaration
    # ===================================================================

    def p_Var_Decl_1(p):
        '''
        Var_Decl : Mod Type Var Var_List  SEMICOLON
        '''
        id = inc()
        p[0] = id
        dot.node(str(id), 'VAR_DECL')
        dot.edge(str(id), str(p[1]))
        dot.edge(str(id), str(p[2]))
        dot.edge(str(id), str(p[3]))
        dot.edge(str(id), str(p[4]))

    def p_Var_Decl_2(p):
        '''
        Var_Decl : Type Var Var_List SEMICOLON
        '''
        id = inc()
        p[0] = id
        dot.node(str(id), 'VAR_DECL')
        dot.edge(str(id), str(p[1]))
        dot.edge(str(id), str(p[2]))
        dot.edge(str(id), str(p[3]))

    def p_Var_Decl_3(p):
        '''
        Var_Decl : Mod Var Var_List SEMICOLON
        '''
        id = inc()
        p[0] = id
        dot.node(str(id), 'VAR_DECL')
        dot.edge(str(id), str(p[1]))
        dot.edge(str(id), str(p[2]))
        dot.edge(str(id), str(p[3]))

    def p_Var_1(p):
        '''
        Var : NAME Array
        '''
        id = inc()
        p[0] = id
        dot.node(str(id), 'VAR')
        id = inc()
        dot.node(str(id), str(p[1]))
        dot.edge(str(p[0]), str(id))
    
    def p_Var_2(p):
        '''
        Var : NAME Array ASSIGN Op_If
        '''
        id = inc()
        p[0] = id
        dot.node(str(id), 'VAR =')
        id = inc()
        dot.node(str(id), str(p[1]))
        dot.edge(str(p[0]), str(id))
        dot.edge(str(p[0]), str(p[4]))

    def p_Array_1(p):
        '''
        Array    : L_BRACKET Expr R_BRACKET
        '''
        id = inc()
        p[0] = id
        dot.node(str(id), 'ARRAY')
        dot.edge(str(id), '[')
        dot.edge(str(id), str(p[2]))
        dot.edge(str(id), ']')
    
    def p_Array_2(p):
        '''
        Array : L_BRACKET R_BRACKET
            | empty
        '''
        p[0] = None

    def p_Var_List_1(p):
        '''
        Var_List :  COMMA Var_Item Var_List
        '''
        id = inc()
        p[0] = id
        dot.node(str(id), 'VAR_LIST')
        dot.edge(str(id), str(p[2]))
        dot.edge(str(id), str(p[3]))

    def p_Var_List_2(p):
        '''
        Var_List : empty
        '''
        p[0] = None

    def p_Var_Item(p):
        '''
        Var_Item : Pointers Var
        '''
        id = inc()
        p[0] = id
        dot.node(str(id), 'VAR_ITEM')
        dot.edge(str(id), str(p[1]))
        dot.edge(str(id), str(p[2]))

    def p_Mod(p):
        '''
        Mod : EXTERN 
            | STATIC
            | REGISTER
            | AUTO
            | VOLATILE
            | CONST
        '''
        id = inc()
        p[0] = id
        dot.node(str(id), 'MOD')
        dot.edge(str(id), str(p[1]))

    # ===================================================================
    # Enumerations
    # ===================================================================

    def p_Enum_Decl(p):
        '''
        Enum_Decl : ENUM NAME L_CURLY Enum_Def R_CURLY SEMICOLON
        '''
        id = inc()
        p[0] = id
        dot.node(str(id), 'ENUM_DECL')
        dot.edge(str(id), 'enum')
        dot.edge(str(id), str(p[2]))
        dot.edge(str(id), str(p[4]))

    def p_Enum_Def_1(p):
        '''
        Enum_Def : Enum_Val COMMA Enum_Def
        '''
        id = inc()
        p[0] = id
        dot.node(str(id), 'ENUM_DEF')
        dot.edge(str(id), str(p[1]))
        dot.edge(str(id), str(p[3]))

    def p_Enum_Def_2(p):
        '''
        Enum_Def : Enum_Val
        '''
        id = inc()
        p[0] = id
        dot.node(str(id), 'ENUM_DEF')
        dot.edge(str(id), str(p[1]))

    def p_Enum_Val_1(p):
        '''
        Enum_Val : NAME
        '''
        id = inc()
        p[0] = id
        dot.node(str(id), 'ENUM_VAL')
        dot.edge(str(id), str(p[1]))

    def p_Enum_Val_2(p):
        '''
        Enum_Val : NAME ASSIGN INTEGER
        '''
        id = inc()
        p[0] = id
        dot.node(str(id), 'ENUM_VAL')
        dot.edge(str(id), '=')
        dot.edge(str(id), str(p[1]))
        dot.edge(str(id), str(p[3]))

    # ===================================================================
    # Types
    # ===================================================================

    def p_Type(p):
        '''
        Type : Base Pointers 
        '''
        id = inc()
        p[0] = id
        dot.node(str(id), 'TYPE')
        dot.edge(str(id), str(p[1]))
        dot.edge(str(id), str(p[2]))

    def p_Base_1(p):
        '''
        Base : Sign Scalar
        '''
        id = inc()
        p[0] = id
        dot.node(str(id), 'BASE')
        dot.edge(str(id), str(p[1]))
        dot.edge(str(id), str(p[2]))

    def p_Base_2(p):
        '''
        Base : STRUCT NAME 
        '''
        id = inc()
        p[0] = id
        dot.node(str(id), 'BASE')
        dot.edge(str(id), 'struct')
        dot.edge(str(id), str(p[1]))

    def p_Base_3(p):
        '''
        Base : STRUCT L_CURLY Struct_Def R_CURLY            
        '''
        id = inc()
        p[0] = id
        dot.node(str(id), 'BASE')
        dot.edge(str(id), 'struct')
        dot.edge(str(id), str(p[3]))

    def p_Base_4(p):
        '''
        Base : UNION NAME
        '''
        id = inc()
        p[0] = id
        dot.node(str(id), 'BASE')
        dot.edge(str(id), 'union')
        dot.edge(str(id), str(p[2]))

    def p_Base_5(p):
        '''
        Base : UNION L_CURLY Struct_Def R_CURLY 
        '''
        id = inc()
        p[0] = id
        dot.node(str(id), 'BASE')
        dot.edge(str(id), 'union')
        dot.edge(str(id), str(p[3]))

    def p_Base_6(p):
        '''
        Base : ENUM NAME 
        '''
        id = inc()
        p[0] = id
        dot.node(str(id), 'BASE')
        dot.edge(str(id), 'enum')
        dot.edge(str(id), str(p[2]))

    def p_Sign_1(p):
        '''
        Sign : SIGNED
            | UNSIGNED
        '''
        id = inc()
        p[0] = id
        dot.node(str(id), 'SIGN')
        dot.edge(str(id), str(p[1]))

    def p_Sign_2(p):
        '''
        Sign : empty
        '''
        p[0] = None

    def p_Scalar(p):
        '''
        Scalar : CHAR
            | INT
            | FLOAT
            | DOUBLE
            | VOID  
        '''
        id = inc()
        p[0] = id
        dot.node(str(id), 'SCALAR')
        id = inc()
        dot.node(str(id), str(p[1]) )
        dot.edge(str(id-1), str(id))

    def p_Pointers_1(p):
        '''
        Pointers : MULTIPLY Pointers
        '''
        id = inc()
        p[0] = id
        dot.node(str(id), 'POINTERS')
        dot.edge(str(id), str(p[1]))
        dot.edge(str(id), str(p[2]))

    def p_Pointers_2(p):
        '''
        Pointers : empty
        '''
        p[0] = None

    # ===================================================================
    # Statements
    # ===================================================================

    def p_Stm_0(p):
        '''
        Stm : PRINTF L_PAR STRING Printf_Params R_PAR SEMICOLON
        '''
        id = inc()
        p[0] = id
        dot.node(str(id), 'PRINTF')
        dot.edge(str(id), str(p[4]))

    def p_Printf_Params_1(p):
        '''
        Printf_Params : COMMA Printf_Param  Printf_Params
        '''
        id = inc()
        p[0] = id
        dot.node(str(id), 'PRINTF_PARAMS')
        dot.edge(str(id), str(p[2]))
        dot.edge(str(id), str(p[3]))
        

    def p_Printf_Params_2(p):
        '''
        Printf_Params : Printf_Param
        '''
        id = inc()
        p[0] = id
        dot.node(str(id), 'PRINTF_PARAMS')
        dot.edge(str(id), str(p[1]))

    def p_Printf_Params_3(p):
        '''
        Printf_Params : empty
        '''
        p[0] = 'NonePrintfParam'

    def p_Printf_Param(p):
        '''
        Printf_Param : Op_Pointer
        '''
        id = inc()
        p[0] = id
        dot.node(str(id), 'PRINTF_PARAM')
        dot.edge(str(id), str(p[1]))

    def p_Stm_01(p):
        '''
        Stm : SCANF L_PAR STRING COMMA Scanf_Param R_PAR SEMICOLON
        '''
        id = inc()
        p[0] = id
        dot.node(str(id), 'SCANF')
        dot.edge(str(id), str(p[3]))
        dot.edge(str(id), str(p[5]))

    def p_Scanf_Param_1(p):
        '''
        Scanf_Param : AND_B NAME
        '''
        id = inc()
        p[0] = id
        dot.node(str(id), 'SCANF_PARAM &')
        dot.edge(str(id), p[2])

    def p_Scanf_Param_2(p):
        '''
        Scanf_Param : NAME
        '''
        id = inc()
        p[0] = id
        dot.node(str(id), 'SCANF_PARAM')
        id = inc()
        dot.node(str(id), p[1])
        dot.edge(str(p[0]), str(id))

########

    def p_Stm_1(p):
        '''
        Stm : Var_Decl
        '''
        id = inc()
        p[0] = id
        dot.node(str(id), 'STM')
        dot.edge(str(id), str(p[1]))
        
    def p_Stm_2(p):
        '''
        Stm : NAME COLON
        '''
        id = inc()
        p[0] = id
        dot.node(str(id), 'STM')
        dot.edge(str(id), str(p[1]))

    def p_Stm_3(p):
        '''
        Stm : IF L_PAR Expr R_PAR Then_Stm ELSE Stm
        '''
        id = inc()
        p[0] = id
        dot.node(str(id), 'STM IF ELSE')
        dot.edge(str(id), str(p[3]))
        dot.edge(str(id), str(p[5]))
        dot.edge(str(id), str(p[7]))

    def p_Stm_7(p):
        '''
        Stm : IF L_PAR Expr R_PAR Stm
        '''
        id = inc()
        p[0] = id
        dot.node(str(id), 'STM IF')
        dot.edge(str(id), str(p[3]))
        dot.edge(str(id), str(p[5]))

    def p_Stm_4(p):
        '''
        Stm : WHILE L_PAR Expr R_PAR Stm 
        '''
        id = inc()
        p[0] = id
        dot.node(str(id), 'STM WHILE')
        dot.edge(str(id), str(p[3]))
        dot.edge(str(id), str(p[5]))

    def p_Stm_5(p):
        '''
        Stm : FOR L_PAR Arg SEMICOLON Arg SEMICOLON Arg R_PAR Stm
        '''
        id = inc()
        p[0] = id
        dot.node(str(id), 'STM FOR')
        dot.edge(str(id), str(p[3]))
        dot.edge(str(id), str(p[5]))
        dot.edge(str(id), str(p[7]))
        dot.edge(str(id), str(p[9]))
    
    def p_Stm_6(p):
        '''
        Stm : Normal_Stm
        '''
        id = inc()
        p[0] = id
        dot.node(str(id), 'STM')
        dot.edge(str(id), str(p[1]))

    def p_Then_Stm_1(p):
        '''
        Then_Stm : IF L_PAR Expr R_PAR Then_Stm ELSE Then_Stm 
        '''
        id = inc()
        p[0] = id
        dot.node(str(id), 'THEN_STM IF ELSE')
        dot.edge(str(id), str(p[3]))
        dot.edge(str(id), str(p[5]))
        dot.edge(str(id), str(p[7]))

    def p_Then_Stm_2(p):
        '''
        Then_Stm : WHILE L_PAR Expr R_PAR Then_Stm 
        '''
        id = inc()
        p[0] = id
        dot.node(str(id), 'THEN_STM WHILE')
        dot.edge(str(id), str(p[3]))
        dot.edge(str(id), str(p[5]))

    def p_Then_Stm_3(p):
        '''
        Then_Stm : FOR L_PAR Arg SEMICOLON Arg SEMICOLON Arg R_PAR Then_Stm
        '''
        id = inc()
        p[0] = id
        dot.node(str(id), 'THEN_STM FOR')
        dot.edge(str(id), str(p[3]))
        dot.edge(str(id), str(p[5]))
        dot.edge(str(id), str(p[7]))
        dot.edge(str(id), str(p[9]))

    def p_Then_Stm_4(p):
        '''
        Then_Stm : Normal_Stm
        '''
        id = inc()
        p[0] = id
        dot.node(str(id), 'THEN_STM')
        dot.edge(str(id), str(p[1]))

    def p_Normal_Stm_1(p):
        '''
        Normal_Stm : DO Stm WHILE L_PAR Expr R_PAR            
        '''
        id = inc()
        p[0] = id
        dot.node(str(id), 'NORMAL_STM DO WHILE')
        dot.edge(str(id), str(p[2]))
        dot.edge(str(id), str(p[5]))

    def p_Normal_Stm_2(p):
        '''
        Normal_Stm : SWITCH L_PAR Expr R_PAR L_CURLY Case_Stms R_CURLY         
        '''
        id = inc()
        p[0] = id
        dot.node(str(id), 'NORMAL_STM SWITCH')
        dot.edge(str(id), str(p[3]))
        dot.edge(str(id), str(p[6]))

    def p_Normal_Stm_3(p):
        '''
        Normal_Stm : Block             
        '''
        id = inc()
        p[0] = id
        dot.node(str(id), 'NORMAL_STM')
        dot.edge(str(id), str(p[1]))

    def p_Normal_Stm_4(p):
        '''
        Normal_Stm : Expr SEMICOLON
        '''
        id = inc()
        p[0] = id
        dot.node(str(id), 'NORMAL_STM')
        dot.edge(str(id), str(p[1]))

    def p_Normal_Stm_5(p):
        '''
        Normal_Stm : GOTO NAME SEMICOLON
        '''
        id = inc()
        p[0] = id
        dot.node(str(id), 'NORMAL_STM GOTO')
        dot.edge(str(id), str(p[2]))
        
    def p_Normal_Stm_6(p):
        '''
        Normal_Stm : BREAK SEMICOLON
        '''
        id = inc()
        p[0] = id
        dot.node(str(id), 'NORMAL_STM BREAK')

    def p_Normal_Stm_7(p):
        '''
        Normal_Stm : CONTINUE SEMICOLON
        '''
        id = inc()
        p[0] = id
        dot.node(str(id), 'NORMAL_STM CONTINUE')
        
    def p_Normal_Stm_8(p):
        '''
        Normal_Stm : RETURN Expr SEMICOLON
        '''
        id = inc()
        p[0] = id
        dot.node(str(id), 'NORMAL_STM RETURN')
        dot.edge(str(p[0]), str(p[2]))

    def p_Normal_Stm_9(p):
        '''
        Normal_Stm : SEMICOLON
        '''
        id = inc()
        p[0] = id
        dot.node(str(id), 'NORMAL_STM ;')

    def p_Arg_1(p):
        '''
        Arg : Expr 
        '''
        id = inc()
        p[0] = id
        dot.node(str(id), 'ARG')
        dot.edge(str(id), str(p[1]))

    def p_Arg_2(p):
        '''
        Arg : empty
        '''
        p[0] = None

    def p_Case_Stms_1(p):
        '''
        Case_Stms : CASE Value COLON Stm_List Case_Stms
        '''
        id = inc()
        p[0] = id
        dot.node(str(id), 'CASE_STMS')
        dot.edge(str(id), 'case')
        dot.edge(str(id), str(p[2]))
        dot.edge(str(id), str(p[4]))
        dot.edge(str(id), str(p[5]))

    def p_Case_Stms_2(p):
        '''
        Case_Stms : DEFAULT COLON Stm_List                  
        '''
        id = inc()
        p[0] = id
        dot.node(str(id), 'CASE_STMS')
        dot.edge(str(id), 'default')
        dot.edge(str(id), str(p[3]))
        
    def p_Case_Stms_3(p):
        '''
        Case_Stms : empty
        '''
        p[0] = None

    def p_Block(p):
        '''
        Block : L_CURLY Stm_List R_CURLY
        '''
        id = inc()
        p[0] = id
        dot.node(str(id), 'BLOCK')
        dot.edge(str(id), str(p[2]))

    def p_Stm_List_1(p):
        '''
        Stm_List  :  Stm Stm_List 
        '''
        id = inc()
        p[0] = id
        dot.node(str(id), 'STM_LIST')
        dot.edge(str(id), str(p[1]))
        dot.edge(str(id), str(p[2]))

    def p_Stm_List_2(p):
        '''
        Stm_List  :  empty  
        '''
        p[0] = None


    # ===================================================================
    # Here begins the C's 15 levels of operator precedence.
    # ===================================================================

    def p_Expr_1(p):
        '''
        Expr : Expr COMMA Op_Assign
        '''
        id = inc()
        p[0] = id
        dot.node(str(id), 'EXPR')
        dot.edge(str(id), str(p[1]))
        dot.edge(str(id), str(p[3]))

    def p_Expr_2(p):
        '''
        Expr : Op_Assign
        '''
        id = inc()
        p[0] = id
        dot.node(str(id), 'EXPR')
        dot.edge(str(id), str(p[1]))


    def p_Op_Assign_1(p):
        '''
        Op_Assign  : Op_If ASSIGN Op_Assign
                    | Op_If APLUS Op_Assign
                    | Op_If AMINUS Op_Assign
                    | Op_If AMULTIPLY Op_Assign
                    | Op_If ADIVIDE Op_Assign
                    | Op_If AXOR Op_Assign
                    | Op_If AAND Op_Assign
                    | Op_If AOR Op_Assign
                    | Op_If ASHIFT_R Op_Assign
                    | Op_If ASHIFT_L Op_Assign
        '''
        id = inc()
        p[0] = id
        dot.node(str(id), 'OP_ASSIGN')
        
        id=inc()
        dot.node(str(id), str(p[2]))

        dot.edge(str(p[0]), str(p[1]))
        dot.edge(str(p[0]), str(id))
        dot.edge(str(p[0]), str(p[3]))

    def p_Op_Assign_2(p):
        '''
        Op_Assign : Op_If
        '''
        id = inc()
        p[0] = id
        dot.node(str(id), 'OP_ASSIGN')
        dot.edge(str(id), str(p[1]))

    def p_Op_If_1(p):
        '''
        Op_If : Op_Or QUESTION Op_If COLON Op_If
        '''
        id = inc() #0
        p[0] = id 
        dot.node(str(id), 'OP_IF')
        id = inc()
        dot.node(str(id), '?')
        id = inc()
        dot.node(str(id), ':')

        dot.edge(str(p[0]), str(p[1]))
        dot.edge(str(p[0]), str(id-1))
        dot.edge(str(p[0]), str(p[3]))
        #dot.edge(str(p[0]), str(p[id]))
        dot.edge(str(p[0]), str(p[5]))




    def p_Op_If_2(p):
        '''
        Op_If : Op_Or
        '''
        id = inc() #0
        p[0] = id 
        dot.node(str(id), 'OP_IF')
        dot.edge(str(p[0]), str(p[1]))

    def p_Op_Or_1(p):
        '''
        Op_Or : Op_Or OR Op_And
        '''
        id = inc() #0
        p[0] = id 
        dot.node(str(id), 'OP_OR')
        id = inc()
        dot.node(str(id), '||')

        dot.edge(str(p[0]), str(p[1]))
        dot.edge(str(p[0]), str(id))
        dot.edge(str(p[0]), str(p[3]))

    def p_Op_Or_2(p):
        '''
        Op_Or : Op_And
        '''
        id = inc() #0
        p[0] = id 
        dot.node(str(id), 'OP_OR')
        dot.edge(str(p[0]), str(p[1]))

    def p_Op_And_1(p):
        '''
        Op_And : Op_And AND Op_BinOR
        '''
        id = inc() #0
        p[0] = id 
        dot.node(str(id), 'OP_AND')
        id = inc()
        dot.node(str(id), '&&')

        dot.edge(str(p[0]), str(p[1]))
        dot.edge(str(p[0]), str(id))
        dot.edge(str(p[0]), str(p[3]))

    def p_Op_And_2(p):
        '''
        Op_And : Op_BinOR
        '''
        id = inc() #0
        p[0] = id 
        dot.node(str(id), 'OP_AND')
        dot.edge(str(p[0]), str(p[1]))

    def p_Op_BinOR_1(p):
        '''
        Op_BinOR : Op_BinOR OR_B Op_BinXOR
        '''
        id = inc() #0
        p[0] = id 
        dot.node(str(id), 'OP_AND')
        id = inc()
        dot.node(str(id), '&&')

        dot.edge(str(p[0]), str(p[1]))
        dot.edge(str(p[0]), str(id))
        dot.edge(str(p[0]), str(p[3]))

    def p_Op_BinOR_2(p):
        '''
        Op_BinOR : Op_BinXOR
        '''
        id = inc() #0
        p[0] = id 
        dot.node(str(id), 'OP_BIN_XOR')
        dot.edge(str(p[0]), str(p[1]))

    def p_Op_BinXOR_1(p):
        '''
        Op_BinXOR : Op_BinXOR XOR_B Op_BinAND
        '''
        id = inc() #0
        p[0] = id 
        dot.node(str(id), 'OP_BIN_OR')
        id = inc()
        dot.node(str(id), '^')

        dot.edge(str(p[0]), str(p[1]))
        dot.edge(str(p[0]), str(id))
        dot.edge(str(p[0]), str(p[3]))

    def p_Op_BinXOR_2(p):
        '''
        Op_BinXOR : Op_BinAND
        '''
        id = inc() #0
        p[0] = id 
        dot.node(str(id), 'OP_BIN_AND')
        dot.edge(str(p[0]), str(p[1]))

    def p_Op_BinAND_1(p):
        '''
        Op_BinAND : Op_BinAND AND_B Op_Equate
        '''
        id = inc() #0
        p[0] = id 
        dot.node(str(id), 'OP_BIN_AND')
        id = inc()
        dot.node(str(id), '&')

        dot.edge(str(p[0]), str(p[1]))
        dot.edge(str(p[0]), str(id))
        dot.edge(str(p[0]), str(p[3]))

    def p_Op_BinAND_2(p):
        '''
        Op_BinAND : Op_Equate
        '''
        id = inc() #0
        p[0] = id 
        dot.node(str(id), 'OP_BIN_AND')
        dot.edge(str(p[0]), str(p[1]))

    def p_Op_Equate_1(p):
        '''
        Op_Equate : Op_Equate EQUAL Op_Compare
            | Op_Equate NOT_EQUAL Op_Compare
        '''
        id = inc() #0
        p[0] = id 
        dot.node(str(id), 'OP_EQUATE')
        id = inc()
        dot.node(str(id), str(p[2]))

        dot.edge(str(p[0]), str(p[1]))
        dot.edge(str(p[0]), str(id))
        dot.edge(str(p[0]), str(p[3]))


    def p_Op_Equate_2(p):
        '''
        Op_Equate : Op_Compare
        '''
        id = inc() #0
        p[0] = id 
        dot.node(str(id), 'OP_EQUATE')
        dot.edge(str(p[0]), str(p[1]))

    def p_Op_Compare_1(p):
        '''
        Op_Compare : Op_Compare LESS  Op_Shift
            | Op_Compare GREATER  Op_Shift
            | Op_Compare LESS_EQUAL Op_Shift
            | Op_Compare GREATER_EQUAL Op_Shift
        '''
        id = inc() #0
        p[0] = id 
        dot.node(str(id), 'OP_COMPARE')
        id = inc()
        dot.node(str(id), str(p[2]))

        dot.edge(str(p[0]), str(p[1]))
        dot.edge(str(p[0]), str(id))
        dot.edge(str(p[0]), str(p[3]))

    def p_Op_Compare_2(p):
        '''
        Op_Compare : Op_Shift
        '''
        id = inc() #0
        p[0] = id 
        dot.node(str(id), 'OP_COMPARE')
        dot.edge(str(p[0]), str(p[1]))

    def p_Op_Shift_1(p):
        '''
        Op_Shift : Op_Shift SHIFT_L Op_Add
            | Op_Shift SHIFT_R Op_Add
        '''
        id = inc() #0
        p[0] = id 
        dot.node(str(id), 'OP_SHIFT')
        id = inc()
        dot.node(str(id), str(p[2]))

        dot.edge(str(p[0]), str(p[1]))
        dot.edge(str(p[0]), str(id))
        dot.edge(str(p[0]), str(p[3]))

    def p_Op_Shift_2(p):
        '''
        Op_Shift : Op_Add
        '''
        id = inc() #0
        p[0] = id 
        dot.node(str(id), 'OP_SHIFT')
        dot.edge(str(p[0]), str(p[1]))

    def p_Op_Add_1(p):
        '''
        Op_Add : Op_Add PLUS Op_Mult
            | Op_Add MINUS Op_Mult
        '''
        id = inc() #0
        p[0] = id 
        dot.node(str(id), 'OP_ADD')
        id = inc()
        dot.node(str(id), str(p[2]))

        dot.edge(str(p[0]), str(p[1]))
        dot.edge(str(p[0]), str(id))
        dot.edge(str(p[0]), str(p[3]))

    def p_Op_Add_2(p):
        '''
        Op_Add : Op_Mult
        '''
        id = inc() #0
        p[0] = id 
        dot.node(str(id), 'OP_ADD')
        dot.edge(str(p[0]), str(p[1]))

    def p_Op_Mult_1(p):
        '''
        Op_Mult : Op_Mult MULTIPLY Op_Unary
            | Op_Mult DIVIDE Op_Unary
            | Op_Mult REMAINDER Op_Unary
        '''
        id = inc() #0
        p[0] = id 
        dot.node(str(id), 'OP_MULT')
        id = inc()
        dot.node(str(id), str(p[2]))

        dot.edge(str(p[0]), str(p[1]))
        dot.edge(str(p[0]), str(id))
        dot.edge(str(p[0]), str(p[3]))

    def p_Op_Mult_2(p):
        '''
        Op_Mult : Op_Unary
        '''
        id = inc() #0
        p[0] = id 
        dot.node(str(id), 'OP_MULT')
        dot.edge(str(p[0]), str(p[1]))

    def p_Op_Unary_1(p):
        '''
        Op_Unary : NOT Op_Unary
            | NOT_B Op_Unary
            | UMINUS Op_Unary
            | MULTIPLY Op_Unary
            | AND_B Op_Unary            
        '''
        id = inc() #0
        p[0] = id 
        dot.node(str(id), 'OP_UNARY')
        id = inc()
        dot.node(str(id), p[1])
        dot.edge(str(p[0]), str(id))

    def p_Op_Unary_2(p):
        '''
        Op_Unary : PLUSPLUS Op_Unary
            | MINUSMINUS Op_Unary
        '''
        id = inc() #0
        p[0] = id 
        dot.node(str(id), 'OP_UNARY')
        id = inc()
        dot.node(str(id), p[1])
        dot.edge(str(p[0]), str(id))

    def p_Op_Unary_3(p):
        '''
        Op_Unary : Op_Pointer PLUSPLUS
            | Op_Pointer MINUSMINUS
        '''
        id = inc() #0
        p[0] = id 
        dot.node(str(id), 'OP_UNARY')
        id = inc()
        dot.node(str(id), p[2])
        dot.edge(str(p[0]), str(p[1]))
        dot.edge(str(p[0]), str(id))

    def p_Op_Unary_4(p):
        '''
        Op_Unary : L_PAR Type R_PAR Op_Unary
        '''
        id = inc() #0
        p[0] = id 
        dot.node(str(id), 'OP_UNARY')
        id = inc()
        dot.node(str(id), p[1])
        dot.edge(str(p[0]), str(id))
        dot.edge(str(p[0]), str(p[4]))

    def p_Op_Unary_5(p):
        '''
        Op_Unary : SIZEOF L_PAR Type R_PAR
        '''
        id = inc() #0
        p[0] = id 
        dot.node(str(id), 'OP_UNARY')
        id = inc()
        dot.node(str(id), p[1])
        dot.edge(str(p[0]), str(id))
        dot.edge(str(p[0]), str(p[3]))

    def p_Op_Unary_6(p):
        '''
        Op_Unary : SIZEOF L_PAR NAME Pointers R_PAR
        '''
        id = inc() #0
        p[0] = id 
        dot.node(str(id), 'OP_UNARY')
        id = inc()
        dot.node(str(id), p[1])
        dot.edge(str(p[0]), str(id))
        dot.edge(str(p[0]), str(p[3]))
        dot.edge(str(p[0]), str(p[4]))

    def p_Op_Unary_7(p):
        '''
        Op_Unary : Op_Pointer
        '''
        id = inc() #0
        p[0] = id 
        dot.node(str(id), 'OP_UNARY')
        dot.edge(str(p[0]), str(p[1]))

    def p_Op_Pointer_1(p):
        '''
        Op_Pointer : Op_Pointer DOT Value
        '''
        id = inc() #0
        p[0] = id 
        dot.node(str(id), 'OP_POINTER .')
        dot.edge(str(p[0]), str(p[1]))
        dot.edge(str(p[0]), str(p[3]))

    def p_Op_Pointer_2(p):
        '''
        Op_Pointer : Op_Pointer ACCESS Value
        '''
        id = inc() #0
        p[0] = id 
        dot.node(str(id), 'OP_POINTER ->')
        dot.edge(str(p[0]), str(p[1]))
        dot.edge(str(p[0]), str(p[3]))

    def p_Op_Pointer_3(p):
        '''
        Op_Pointer : Op_Pointer L_BRACKET Expr R_BRACKET
        '''
        id = inc() #0
        p[0] = id 
        dot.node(str(id), 'OP_POINTER []')
        dot.edge(str(p[0]), str(p[1]))
        dot.edge(str(p[0]), str(p[3]))

    def p_Op_Pointer_4(p):
        '''
        Op_Pointer : Value
        '''
        id = inc() #0
        p[0] = id 
        dot.node(str(id), 'OP_POINTER')
        dot.edge(str(p[0]), str(p[1]))

    def p_Value_1(p):
        '''
        Value : INTEGER
            | STRING
            | CHARACTER
            | DECIMAL
            | NAME
        '''
        id = inc() #0
        p[0] = id 
        dot.node(str(id), str(p[1]))

    def p_Value_2(p):
        '''
        Value : NAME L_PAR Expr R_PAR
        '''
        id = inc() #0
        p[0] = id 
        dot.node(str(id), 'VALUE call')
        dot.edge(str(p[0]), str(p[1]))
        dot.edge(str(p[0]), str(p[3]))

    def p_Value_3(p):
        '''
        Value : NAME L_PAR R_PAR
        '''
        id = inc() #0
        p[0] = id 
        dot.node(str(id), 'VALUE call')
        dot.edge(str(p[0]), str(p[1]))

    def p_Value_4(p):
        '''
        Value : L_PAR Expr R_PAR
        '''
        p[0] = p[2]
        id = inc() #0
        p[0] = id 
        dot.node(str(id), 'VALUE')
        dot.edge(str(p[0]), str(p[2]))
      
    #Empty production
    def p_empty(p):
        '''
        empty :
        '''
        p[0] = None

    def p_error(p):
        pass

      

    from .ply import yacc as yacc
    
    parser = yacc.yacc()
    ast = parser.parse(entrada,tracking=True)
    
    
    dotFile = str(dot.source)
    newDotFile = dotFile.replace('-- None', '')


    tree = pydotplus.graph_from_dot_data(newDotFile)
    #print(dot.source)
    tree.write_pdf('AST.pdf')
    
    ast = parser.parse(entrada)

    return ast