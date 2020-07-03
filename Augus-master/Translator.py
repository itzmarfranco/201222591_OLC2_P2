from Instruction import *
from Expression import *

from SymbolTable import Table, Symbol
from Error import Error, ErrorList

import re

from graphviz import Digraph
import pydotplus

#method to wrote file
def write3D(str):
    f = open('3d.augus', 'a+')
    f.write(str)
    f.close()


l = 0 # counter for labels
t = 0 # counter for $t
a = 0 # counter for $a
v = 0 # counter for $v


def create_l():
    global l
    l = l+1
    return 'label'+str(l)

def create_t():
    global t
    t = t+1
    return '$t'+str(t)

def create_a():
    global a
    a = a+1
    return '$a'+str(a)

def create_v():
    global v
    v = v+1
    return '$v'+str(v)


class code3D():
    def __init__(self):
        self.code = ''
        self.temp = ''


result = code3D()

functionList = [] # list with all functions declared

callList = [] # list with all funcions called

tsStack = [] # stack with ts for each enviroment

breakStack = [] # stack to handle cycles and switch break statement

continueStack = [] # stack to handle cycles continue statement

semanticErrors = ErrorList([])


#Main translate method
def translate(instructions):

    global result
    global tsStack
    # global ts
    tsStack.clear()
    ts = Table([])
    tsStack.append(ts)

    result.code += 'main:\n'

    for i in instructions:
        if isinstance(i, function):
            translateFunction(i)
        elif isinstance(i, struct):
            translateStruct(i)
        elif isinstance(i, union):
            translateUnion(i)
        elif isinstance(i, enum):
            translateEnum(i)
        elif isinstance(i, definition):
            translateVarDec(i)

    result.code += 'exit;\n\n\n#############\n'
    if len(callList) > 0:
        for f in callList:
            translateFunctionCalled(f[0], f[1], f[2], f[3])
            
    print(result.code)
    print('###################################\nTABLAS DE SIMBOLOS')
    for t in tsStack:
        t.print()
        print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& FIN &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")

    semanticErrorReport()
    
    return result.code

###################################

def translateBlock(b):
    global result
    if b != None:
        for i in b:
            if isinstance(i, printf): translatePrintf(i)
            elif isinstance(i, scanf): translateScanf(i)
            elif isinstance(i, Goto): translateGoto(i)
            elif isinstance(i, Label): translateLabel(i)
            elif isinstance(i, Break): translateBreak(i)
            elif isinstance(i, Continue): translateContinue(i)
            elif isinstance(i, Return): translateReturn(i)
            elif isinstance(i, ExpresionList): translateExpressionList(i.expressions[0])
            elif isinstance(i, definition): translateVarDec(i)
            elif isinstance(i, Variable): translateVariable(i)
            elif isinstance(i, iff):
                ts = Table([])
                tsStack.append(ts)
                result.code += '# INICIO DE IF\n'
                translateIf(i)
                result.code += '# FIN DE IF\n'
                tsStack.pop()
            elif isinstance(i, ifelse):
                ts = Table([])
                tsStack.append(ts)
                result.code += '# INICIO DE IF-ELSE\n'
                translateIfElse(i)
                result.code += '# FIN DE IF-ELSE\n'
                tsStack.pop()
            elif isinstance(i, whilee):
                ts = Table([])
                tsStack.append(ts)
                result.code += '# INICIO DE WHILE\n'
                translateWhile(i)
                result.code += '# FIN DE WHILE\n'
                tsStack.pop()
            elif isinstance(i, dowhile):
                ts = Table([])
                tsStack.append(ts)
                result.code += '# INICIO DE DO-WHILE\n'
                translateDoWhile(i)
                result.code += '# FIN DE DO-WHILE\n'
                tsStack.pop()
            elif isinstance(i, forr):
                ts = Table([])
                tsStack.append(ts)
                result.code += '# INICIO DE FOR\n'
                translateFor(i)
                result.code += '# FIN DE FOR\n'
                tsStack.pop()
            elif isinstance(i, Switch):
                ts = Table([])
                tsStack.append(ts)
                result.code += '# INICIO DE SWITCH\n'
                translateSwitch(i)
                result.code += '# INICIO DE SWITCH\n'
                tsStack.pop()
            elif isinstance(i, Call):
                translateCall(i)

def translateFunction(f):
    if(f.id == 'main'):
        global tsStack
        # main's ts
        ts = Table([])
        tsStack.append(ts) 
        if f.body != None:
            #ts for main
            translateBlock(f.body)
        else:
            # nothing to translate
            pass

        tsStack.pop()
    else:
        # translate function that is being called
        global functionList
        functionList.append(f)

def translateStruct(s):
    print('traduciendo struct')
    pass

def translateUnion(u):
    print('traduciendo union')
    pass

def translateEnum(e):
    print('traduciendo enum')
    pass

def translateVarDec(v):
    # store in current peek ts 
    global tsStack
    global result
    tempTS = tsStack[len(tsStack)-1] # acceso al entorno actual
    for var in v.id_value: # int b=8 a=9, c=suma();
        if not tsStack[len(tsStack)-1].isSymbolInTable(var):
            translateExpressionList(var.exp)
            var3d = create_t()
            if var.exp != None:
                result.code += var3d + ' = ' + result.temp + ';\n'
            else:
                result.code += var3d + ' = 0;\n'
            l = 1
            if var.array != None: l = 2
            sym = Symbol(var.id, v.varType, var.exp, l, var3d)
            tsStack[len(tsStack)-1].add(sym)
        else:
            print('Error. La variable ya existe:', var)
            e = Error('La variable '+str(var)+' ya existe', 0, 0)
            global semanticErrors
            semanticErrors.add(e)

 ####################################       

def translatePrintf(i):
    global result
    global tsStack
    data = i.string
    parameters = i.parameters
    splittedData = re.split('%c|%s|%d|%s', data)
    if len(parameters) == 0:
        result.code += 'print(\"' + str(data) + '\");\n'
    else:
        #get values for elements in parameters
        valueList = []
        for p in parameters:
            if isPrimitive(p): valueList.append(p.val)
            else:
                tsIndex = len(tsStack)-1
                while tsIndex >= 0:
                    if isinstance(p, Variable):
                        if tsStack[tsIndex].isSymbolInTable(p.id):
                            sym = tsStack[tsIndex].get(p.id)
                            translateExpressionList(sym.value)
                            result.code += 'print(' + result.temp + ');\n'
                    elif isinstance(p,Call):
                        pass

                    tsIndex -= 1

        newData = weave(splittedData, valueList)
        resultString = ''
        for s in newData:
            resultString += str(s)
        result.code += 'print(\"' + resultString + '\");\n'
    
    
def weave(list1, list2):
    result = []
    i = 0
    while i <= len(list1):
        try:
            result.append(list1[i])
            result.append(list2[i])
            i += 1
            if i == len(list2):
                result = result + list1[i::]
                break
        except:
            pass
        i += 1
    
    return result
 
def translateScanf(i):
    global result
    global tsStack

    string = i.string
    var = i.parameter[1]
    result.code += 'print(\"' + string + '\");\n'
    tsIndex = len(tsStack)-1
    while tsIndex >= 0:
        if tsStack[tsIndex].isSymbolInTable(var):
            sym = tsStack[tsIndex].get(var)
            result.code += sym.varName + ' = read();\n'
            result.temp = sym.varName
        else:
            global semanticErrors
            e = Error('No existe la variable para SCANF: '+str(var)+'.',0,0)
            semanticErrors.add(e)

        tsIndex -= 1
    

def translateGoto(i):
    global result
    result.code += 'goto ' + i.ret + ';\n'

def translateLabel(i):
    global result
    result.code += str(i.label) + ':\n'

def translateBreak(i):
    global result
    global breakStack
    # if continueStack has elements, there is a valid enviroment for the continue statement
    if len(breakStack) > 0:
        index = len(breakStack)-1
        label = breakStack[index]
        result.code += 'goto ' + label + ';\n'
    else:
        # Error. Sentencia break en entorno inválido
        print('Error. Sentencia break en entorno inválido')
        e = Error('Error. Sentencia break en entorno inválido', 0, 0)
        global semanticErrors
        semanticErrors.add(e)

def translateContinue(i):
    global result
    global continueStack
    # if continueStack has elements, there is a valid enviroment for the continue statement
    if len(continueStack) > 0:
        index = len(continueStack)-1
        label = continueStack[index]
        result.code += 'goto ' + label + ';\n'
    else:
        # Error. Sentencia break en entorno inválido
        print('Error. Sentencia continue en entorno inválido')
        e = Error('Error. Sentencia break en entorno inválido', 0, 0)
        global semanticErrors
        semanticErrors.add(e)


def translateReturn(i):
    global result
    result.code += 'return 0;\n'

    
def translateVariable(i):
    global tsStack
    global result
    # get variable $tn value and set it to result
    auxStack = []
    found = False
    while len(tsStack)>0:
        ts = tsStack.pop()
        auxStack.append(ts)
        if ts.isSymbolInTable(i.id): #var is in ts
            var3dName = ts.get(i.id).varName #varName is the 3D name for the variable
            result.temp = var3dName
            #print('variable encontrada', var3dName)
            found = True
            break

    if len(auxStack)>0:
        while True:
            tsStack.append(auxStack.pop())
            if len(auxStack) == 0: break

    if(not found):
        print("Traduciendo variable. No existe la variable: ", i.id)
        e = Error('No exite la variable utilizada'+str(i.id)+'.', 0, 0)
        global semanticErrors
        semanticErrors.add(e)


def translateIf(i):
    global result
    global tsStack

    exp = i.condition.expressions[0]
    translateExpressionList(exp)

    trueLabel = create_l()
    result.code += 'if(' + str(result.temp) + ') goto ' + trueLabel + ';\n'
    falseLabel = create_l()
    result.code += 'goto ' + falseLabel + ';\n'
    result.code += trueLabel + ':\n'
    # True instructions
    if i.statements != None:
        translateBlock(i.statements)
    
    result.code += falseLabel + ':\n'

def translateIfElse(i):
    global result
    exp = i.condition.expressions[0]
    translateExpressionList(exp)

    trueLabel = create_l()
    result.code += 'if(' + str(result.temp) + ') goto ' + trueLabel + ';\n'
    falseLabel = create_l()
    exitLabel = create_l()
    result.code += 'goto ' + falseLabel + ';\n'
    result.code += trueLabel + ':\n'
    # True instructions
    if i.statementsTrue != None:
        translateBlock(i.statementsTrue)

    result.code += 'goto ' + exitLabel + ';\n'

    result.code += falseLabel + ':\n'
    if i.statementsFalse != None:
        translateBlock(i.statementsFalse)

    result.code += exitLabel + ':\n'

def translateWhile(i):
    global result
    exp = i.condition.expressions[0]
    stm = i.statements
    returnLabel = create_l() 
    result.code += returnLabel + ':\n' # ret:
    translateExpressionList(exp) # t0 = exp    
    trueLabel = create_l()
    exitLabel = create_l()
    result.code += 'if(' + str(result.temp) + ') goto ' + trueLabel + ';\n' # if(t0) goto L1;
    result.code += 'goto ' + exitLabel + ';\n' #goto L2;
    result.code += trueLabel + ':\n' # L1:
    ####
    # add labels to the break and continue stacks
    global breakStack
    global continueStack
    breakStack.append(exitLabel)
    continueStack.append(returnLabel)
    ####
    translateBlock(stm) #STM
    ###
    # remove labels from break and continue stacks
    breakStack.pop()
    continueStack.pop()
    ###
    result.code += 'goto ' + returnLabel + ';\n' # goto ret;
    result.code += exitLabel + ':\n' # L2:

def translateDoWhile(i):
    exp = i.condition.expressions[0]
    returnLabel = create_l()
    result.code += returnLabel + ':\n'
    stm = i.statements
    translateExpressionList(exp)
    temp = result.temp
    exitLabel = create_l()
    
    ####
    # add labels to the break and continue stacks
    global breakStack
    global continueStack
    breakStack.append(exitLabel)
    continueStack.append(returnLabel)
    ####
    translateBlock(stm) #STM
    ###
    # remove labels from break and continue stacks
    breakStack.pop()
    continueStack.pop()
    ###
    result.code += 'if(' + str(temp) + ') goto ' + returnLabel + ';\n'
    result.code += 'goto ' + exitLabel + ';\n'
    result.code += exitLabel + ':\n'

def translateFor(i):
    global result
    arg1 = i.arg1.expressions[0]
    arg2 = i.arg2.expressions[0]
    arg3 = i.arg3.expressions[0]
    translateExpressionList(arg1) # t0 = arg1
    returnLabel = create_l()
    result.code += returnLabel + ':\n'
    translateExpressionList(arg2) # t1 = arg2
    arg2temp = result.temp
    trueLabel = create_l()
    exitLabel = create_l()
    result.code += 'if(' + str(arg2temp) + ') goto ' + trueLabel + ';\n'
    result.code += 'goto ' + exitLabel + ';\n'
    result.code += trueLabel + ':\n'
    ####
    # add labels to the break and continue stacks
    global breakStack
    global continueStack
    breakStack.append(exitLabel)
    continueStack.append(returnLabel)
    ####
    translateBlock(i.statements) #STM
    ###
    # remove labels from break and continue stacks
    breakStack.pop()
    continueStack.pop()
    ###
    translateExpressionList(arg3)
    result.code += 'goto ' + returnLabel + ';\n'
    result.code += exitLabel + ':\n'


def translateSwitch(i):
    global result
    global breakStack
    # translate case value
    # if (switchCondition == case value) goto CASE1
    # goto CASE2 (can be the exit label. Update where needed)
    # CASE1:
    # translate case statements
    # CASE2:
    # repeat
    translateExpressionList(i.condition)
    switchID = result.temp
    exitLabel = create_l()
    breakStack.append(exitLabel)
    if i.cases != None:
        for case in i.cases:
            if case.value == 'default':
                translateBlock(case.statements)
            else:
                translateExpressionList(case.value)
                caseValue = result.temp
                trueLabel = create_l()
                #falseLabel = create_l()
                result.code += 'if(' + switchID + ' == ' + caseValue + ') goto ' + trueLabel + ';\n'
                #result.code += 'goto ' + falseLabel + ';\n'
                result.code += trueLabel + ':\n'
                translateBlock(case.statements)
                #result.code += 'goto ' + falseLabel + ';\n'
    breakStack.pop()
    result.code += exitLabel + ':\n'
###################################
def translateExpressionList(e):
    if e != None:
        if isinstance(e, AssignOperation): translateAssignOperation(e)
        elif isinstance(e, TernaryOperation): translateTernaryOperation(e)
        elif isinstance(e, LogicalOperation): translateLogicalOperation(e)
        elif isinstance(e, BitwiseOperation): translateBitwiseOperation(e)
        elif isinstance(e, RelationalOperation): translateRelationalOperation(e)
        elif isinstance(e, ShiftOperation): translateShiftOperation(e)
        elif isinstance(e, ArithmeticOperation): translateArithmeticOperation(e)
        elif isinstance(e, UnaryOperation): translateUnaryOperation(e)
        elif isinstance(e, PreOperation): translatePreOperation(e)
        elif isinstance(e, PostOperation): translatePostOperation(e)
        elif isinstance(e, Cast): translateCast(e)
        elif isinstance(e, Sizeof): translateSizeof(e)
        elif isinstance(e, Integer): translateInteger(e)
        elif isinstance(e, String): translateString(e)
        elif isinstance(e, Character): translateCharacter(e)
        elif isinstance(e, Float): translateFloat(e)
        elif isinstance(e, Variable): translateVariable(e)
        elif isinstance(e, Call): translateCall(e)
    elif e == None:
        pass

###################################
def translateAssignOperation(exp):
    global result
    global tsStack
    #si es '=', recuperar el temporal de op1. Buscar en todas las tablas de símbolos
    if exp.operator == '=':
        # get $t var for exp.op1
        tsIndex = len(tsStack)-1 #last ts in the stack (current)
        while(tsIndex >= 0):
            if tsStack[tsIndex].isSymbolInTable(exp.op1.id): # var is in current TS. Update
                sym = tsStack[tsIndex].get(exp.op1.id) # symbol for exp.op1.id
                var3dName = sym.varName # $t name for symbol
                tsStack[tsIndex].update(exp.op1.id, exp.op2) #update symbol
                translateExpressionList(exp.op2)
                result.code += var3dName + ' = ' + result.temp + ';\n'
                result.temp = var3dName # useless, really
                break
            else:
                # not in current TS. Search in the next
                tsIndex -= 1

    #si no es '=' crear expresión con exp.op1 exp.op2 y op dependiendo del exp.op
    else:
        if exp.operator == '+=':
            tempArithmetic = ArithmeticOperation(exp.op1, exp.op2, '+')
            tempAssign = AssignOperation(exp.op1, tempArithmetic, '=')
            translateExpressionList(tempAssign)
        elif exp.operator == '-=':
            tempArithmetic = ArithmeticOperation(exp.op1, exp.op2, '-')
            tempAssign = AssignOperation(exp.op1, tempArithmetic, '=')
            translateExpressionList(tempAssign)
        elif exp.operator == '*=':
            tempArithmetic = ArithmeticOperation(exp.op1, exp.op2, '*')
            tempAssign = AssignOperation(exp.op1, tempArithmetic, '=')
            translateExpressionList(tempAssign)
        elif exp.operator == '/=':
            tempArithmetic = ArithmeticOperation(exp.op1, exp.op2, '%')
            tempAssign = AssignOperation(exp.op1, tempArithmetic, '=')
            translateExpressionList(tempAssign)
        elif exp.operator == '%=':
            tempArithmetic = ArithmeticOperation(exp.op1, exp.op2, '%')
            tempAssign = AssignOperation(exp.op1, tempArithmetic, '=')
            translateExpressionList(tempAssign)
        elif exp.operator == '^=':
            tempArithmetic = BitwiseOperation(exp.op1, exp.op2, '^')
            tempAssign = AssignOperation(exp.op1, tempArithmetic, '=')
            translateExpressionList(tempAssign)
        elif exp.operator == '&=':
            tempArithmetic = BitwiseOperation(exp.op1, exp.op2, '&')
            tempAssign = AssignOperation(exp.op1, tempArithmetic, '=')
            translateExpressionList(tempAssign)
        elif exp.operator == '|=':
            tempArithmetic = BitwiseOperation(exp.op1, exp.op2, '|')
            tempAssign = AssignOperation(exp.op1, tempArithmetic, '=')
            translateExpressionList(tempAssign)
        elif exp.operator == '>>=':
            tempArithmetic = ShiftOperation(exp.op1, exp.op2, '>>')
            tempAssign = AssignOperation(exp.op1, tempArithmetic, '=')
            translateExpressionList(tempAssign)
        elif exp.operator == '<<=':
            tempArithmetic = ShiftOperation(exp.op1, exp.op2, '<<')
            tempAssign = AssignOperation(exp.op1, tempArithmetic, '=')
            translateExpressionList(tempAssign)
        

def translateTernaryOperation(exp):
    global result
    # op1?op2:op3;
    trueLabel = create_l()
    falseLabel = create_l()
    exitLabel = create_l()
    conditionT = exp.op1.expressions
    translateExpressionList(conditionT[0])
    cond = result.temp
    result.code += 'if( ' + cond + ' ) goto ' + trueLabel + ';\n'
    result.code += 'goto ' + falseLabel + ';\n'
    result.code += trueLabel + ':\n'
    translateExpressionList(exp.op2)
    resultName = result.temp
    result.code += resultName + ' = ' + result.temp + ';\n'
    result.code += 'goto ' + exitLabel + ';\n'
    result.code += falseLabel + ':\n'
    translateExpressionList(exp.op3)
    result.code += resultName + ' = ' + result.temp + ';\n' 
    result.code += 'goto ' + exitLabel + ';\n'
    result.code += exitLabel + ':\n'
    
def translateLogicalOperation(exp):
    global result
    translateExpressionList(exp.op1)
    t1 = result.temp
    translateExpressionList(exp.op2)
    t2 = result.temp
    t3 = create_t()
    result.code += t3 + ' = ' + t1 + ' ' + str(exp.operator) + ' ' + t2 + ';\n'
    result.temp = t3


def translateBitwiseOperation(exp):
    global result
    translateExpressionList(exp.op1)
    t1 = result.temp
    translateExpressionList(exp.op2)
    t2 = result.temp
    t3 = create_t()
    result.code += t3 + ' = ' + t1 + ' ' + str(exp.operator) + ' ' + t2 + ';\n'
    result.temp = t3

def translateRelationalOperation(exp):
    global result
    translateExpressionList(exp.op1)
    t1 = result.temp
    translateExpressionList(exp.op2)
    t2 = result.temp
    t3 = create_t()
    result.code += t3 + ' = ' + t1 + ' ' + str(exp.operator) + ' ' + t2 + ';\n'
    result.temp = t3

def translateShiftOperation(exp):
    global result
    translateExpressionList(exp.op1)
    t1 = result.temp
    translateExpressionList(exp.op2)
    t2 = result.temp
    t3 = create_t()
    result.code += t3 + ' = ' + t1 + ' ' + str(exp.operator) + ' ' + t2 + ';\n'
    result.temp = t3

def translateArithmeticOperation(exp):
    global result
    translateExpressionList(exp.op1)
    t1 = result.temp
    translateExpressionList(exp.op2)
    t2 = result.temp
    t3 = create_t()
    result.code += t3 + ' = ' + t1 + ' ' + str(exp.operator) + ' ' + t2 + ';\n'
    result.temp = t3

def translateUnaryOperation(exp):
    global result
    if exp.op == '!' or exp.op == '~' or exp.op == '-':    
        translateExpressionList(exp.val)
        t = create_t()
        result.code += t + ' = '+ str(exp.op) + result.temp + ';\n'
        result.temp = t
    elif exp.op == '*':
        pass
    elif exp.op == '&':
        pass

######################################
def translatePreOperation(exp):
    translatePostOperation(exp)

def translatePostOperation(exp):    
    if isinstance(exp.val, Variable): # x++; search x in ts's
        global tsStack
        auxStack = [] # auxiliar stack
        found = False # was variable found
        varName = exp.val.id
        while len(tsStack)>0:
            ts = tsStack.pop()
            auxStack.append(ts)
            if ts.isSymbolInTable(varName): #var is in ts
                var3dName = ts.get(varName).varName #varName is the 3D name for the variable
                global result
                op = ''
                if exp.op == '++': op = '+'
                else: op = '-'
                result.code += var3dName + ' = ' + var3dName + ' ' + op + ' 1' + ';\n'
                found = True
                break
            else: #var is not in current ts. Get next
                # save previous ts
                # auxStack.append(ts)
                # try again :)
                pass
        # return popped ts's to tsStack
        if len(auxStack)>0:
            while True:
                tsStack.append(auxStack.pop())
                if len(auxStack) == 0: break

        if(not found):
            print("Traduciendo pre/post. No existe la variable:", exp.val)
            e = Error('No existe la variable para operación pre/post: '+str(exp.val)+'.', 0, 0)
            global semanticErrors
            semanticErrors.add(e)

                       

def translateSizeof(exp):
    global result
    t = create_t()
    if exp.varType == 'int':
        result.code += t + ' = ' + '4' + ';\n'
    elif exp.varType == 'float':
        result.code += t + ' = ' + '4' + ';\n'
    elif exp.varType == 'char':
        result.code += t + ' = ' + '1' + ';\n'
    else:
        result.code += t + ' = ' + '0' + ';\n'
    result.temp = t

def translateCast(exp):
    global result
    translateExpressionList(exp.exp)
    result.code += '(' + str(exp.varType) + ')' + str(result.temp) + ';\n'

def translateInteger(exp):
    global result
    t = create_t()
    result.code += t + ' = ' + str(exp.val) + ';\n'
    result.temp = t

def translateString(exp):
    global result
    t = create_t()
    result.code += t + ' = \"' + exp.val + '\";\n'
    result.temp = t

def translateCharacter(exp):
    global result
    t = create_t()
    result.code += t + ' = \'' + exp.val + '\';\n'
    result.temp = t

def translateFloat(exp): # 5.69785
    global result
    t = create_t()
    result.code += t + ' = ' + str(exp.val) + ';\n'
    result.temp = t

def translateCall(exp): # func(params)
    #declarar parámetros
    global result
    global callList
    id = exp.id
    params = exp.parameters
    params3d = []
    if params != None:
        for p in params:
            a = create_a()
            # add parameter to 3d code
            result.code += a + ' = ' + str(p.id) + ' ;' + '\n'
            # add parameter to the call
            params3d.append(a)
        # return label for function
        cal = create_l()
        ret = create_l()
        result.code += 'goto ' + cal + ';\n'
        # translate function with id = id
        if len(functionList) > 0:
            for f in functionList:
                if f.id == id:
                   callList.append((f, params3d, cal, ret))
                   
    result.code += ret + ':' + '\n'


def translateFunctionCalled(f, parameters, callLabel , returnLabel):
    global result
    result.code += callLabel + ':\n'
    # replace variables
    replaceVariables(f, parameters)
    result.code += 'goto ' + str(returnLabel) + ';\n'
    pass

def replaceVariables(function, parameters):
    for a in function.parameters:
        print(a.id)

    for b in parameters:
        print(b)
    pass
    

def isPrimitive(i):
    if isinstance(i, Integer): return True
    elif isinstance(i, Float): return True
    elif isinstance(i, Character): return True
    elif isinstance(i, String): return True
    else: return False


def semanticErrorReport():
    global semanticErrors
    dotDataErrors = 'digraph{tbl[shape=plaintext\nlabel=<<table><tr><td colspan=\'3\'>Reporte de errores</td></tr>'
    dotDataErrors = dotDataErrors + '<tr><td>Error</td><td>Tipo</td><td>Linea</td></tr>'
    for e in semanticErrors.errors:
        dotDataErrors += '<tr><td>'+str(e.value)+'</td><td>Semantico</td><td>'+str(e.line)+'</td></tr>'

    dotDataErrors = dotDataErrors + '</table>>];}'

    errorGraph = pydotplus.graph_from_dot_data(dotDataErrors)
    errorGraph.write_pdf('Reporte_Errores_S.pdf')