from .Instruction import *
from .Expression import *

from .SymbolTable import Table, Symbol

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


#Main translate method
def translate(instructions):
    global result
    global tsStack
    # global ts
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
    print('#############\nTABLAS DE SIMBOLOS')
    for t in tsStack:
        t.print()
        print("&&&&&&&&&&&&&&")

###################################

def translateBlock(b):
    if b != None:
        for i in b:
            if isinstance(i, printf): translatePrintf(i)
            elif isinstance(i, scanf): translateScanf(i)
            elif isinstance(i, Goto): translateGoto(i)
            elif isinstance(i, Break): translateBreak(i)
            elif isinstance(i, Continue): translateContinue(i)
            elif isinstance(i, Return): translateReturn(i)
            elif isinstance(i, ExpresionList): translateExpressionList(i.expressions[0])
            elif isinstance(i, definition): translateVarDec(i)
            elif isinstance(i, Variable): translateVariable(i)
            elif isinstance(i, iff):
                ts = Table([])
                tsStack.append(ts)
                translateIf(i)
                tsStack.pop()
            elif isinstance(i, ifelse):
                ts = Table([])
                tsStack.append(ts)
                translateIfElse(i)
                tsStack.pop()
            elif isinstance(i, whilee):
                ts = Table([])
                tsStack.append(ts)
                translateWhile(i)
                tsStack.pop()
            elif isinstance(i, dowhile):
                ts = Table([])
                tsStack.append(ts)
                translateDoWhile(i)
                tsStack.pop()
            elif isinstance(i, forr):
                ts = Table([])
                tsStack.append(ts)
                translateFor(i)
                tsStack.pop()
            elif isinstance(i, switch):
                ts = Table([])
                tsStack.append(ts)
                translateSwitch(i)
                tsStack.pop()
            elif isinstance(i, Call):
                translateCall(i)

def translateFunction(f):
    if(f.id == 'main'):
        global tsStack
        ts = Table([])
        tsStack.append(ts) # push ts
        if f.body != None:
            #ts for main
            translateBlock(f.body)
            tsStack.pop()
        else:
            # nothing to translate
            pass
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
    tempTS = tsStack.pop()
    for var in v.id_value: # int b=8 a=9, c=suma();
        #translate var.exp
        translateExpressionList(var.exp)
        ##################
        var3d = create_t()
        if var.exp != None:
            result.code += var3d + ' = ' + result.temp + ';\n'
        else:
            result.code += var3d + ';\n'
        sym = Symbol(var.id, v.varType, var.exp, 1, var3d)
        tempTS.add(sym)

    tsStack.append(tempTS)
    
###################################
def translatePrintf(i):
    print('traduciendo printf')
    pass

def translateScanf(i):
    print('traduciendo scanf')
    pass

def translateGoto(i):
    pass

def translateBreak(i):
    pass

def translateContinue(i):
    pass

def translateReturn(i):
    pass

    
def translateVariable(i):
    global tsStack
    global result
    #ts = tsStack.pop()
    # if not ts.isSymbolInTable(i.id):
    #     sym = Symbol(i.id, i.)

    # else:
    #     # error. La variable ya existe
    #     pass

def translateIf(i):
    global result
    global tsStack

    exp = i.condition.expressions[0]
    translateExpressionList(exp)

    trueLabel = create_l()
    result.code += 'if(' + str(result.temp) + ') goto ' + trueLabel + ';\n'
    falseLabel = create_l()
    result.code += 'goto ' + falseLabel + '\n'
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
    result.code += 'goto ' + falseLabel + ':\n'
    result.code += trueLabel + ':\n'
    # True instructions
    if i.statementsTrue != None:
        translateBlock(i.statementsTrue)

    result.code += 'goto ' + exitLabel + ':\n'

    result.code += falseLabel + ':\n'
    if i.statementsFalse != None:
        translateBlock(i.statementsFalse)

    result.code += exitLabel + ':\n'

def translateWhile(i):
    global result
    exp = i.condition.expressions[0]
    stm = i.statements
    translateExpressionList(exp) # t0 = exp
    returnLabel = create_l() 
    result.code += returnLabel + ':\n' # ret:
    trueLabel = create_l()
    exitLabel = create_l()
    result.code += 'if(' + str(result.temp) + ') goto ' + trueLabel + ';\n' # if(t0) goto L1;
    result.code += 'goto ' + exitLabel + ':\n' #goto L2;
    result.code += trueLabel + ':\n' # L1:

    translateBlock(stm) #STM
    result.code += 'goto ' + returnLabel + ':\n' # goto ret;
    result.code += exitLabel + ':\n' # L2:

def translateDoWhile(i):
    exp = i.condition.expressions[0]
    stm = i.statements
    translateExpressionList(exp)
    temp = result.temp
    returnLabel = create_l()
    result.code += returnLabel + ':\n'
    translateBlock(stm)
    result.code += 'if(' + str(temp) + ') goto ' + returnLabel + ';\n'
    exitLabel = create_l()
    result.code += 'goto ' + exitLabel + ':\n'
    result.code += exitLabel + ':\n'

def translateFor(i):
    global result
    arg1 = i.arg1.expressions[0]
    arg2 = i.arg2.expressions[0]
    arg2temp = result.temp
    arg3 = i.arg3.expressions[0]
    translateExpressionList(arg1) # t0 = arg1
    translateExpressionList(arg2) # t1 = arg2
    # if arg1/arg2 have variables, should be stored in ts
    returnLabel = create_l()
    result.code += returnLabel + ':\n'
    L1 = create_l()
    L2 = create_l()
    result.code += 'if(' + str(arg2temp) + ') goto ' + L1 + ';\n'
    result.code += 'goto ' + L2 + ';\n'
    result.code += L1 + ':\n'
    translateBlock(i.statements)
    translateExpressionList(arg3)
    result.code += 'goto ' + returnLabel + ';\n'


def translateSwitch(i):
    print('traduciendo switch')
    pass
###################################
def translateExpressionList(e):
    if e != None:
        if isinstance(e, AssignOperation): print('ASIGNACION', str(e.op1), str(e.operator), str(e.op2))
        elif isinstance(e, TernaryOperation): print('TERNARIA', str(e.op1), str(e.op2), str(e.op3))
        elif isinstance(e, LogicalOperation): print('LOGICA', str(e.op1), str(e.operator), str(e.op2))
        elif isinstance(e, BitwiseOperation): print('BIT A BIT', str(e.op1), str(e.operator), str(e.op2))
        elif isinstance(e, RelationalOperation): print('RELACIONAL', str(e.op1), str(e.operator), str(e.op2))
        elif isinstance(e, ShiftOperation): print('DESPLAZAMIENTO', str(e.op1), str(e.operator), str(e.op2))
        elif isinstance(e, ArithmeticOperation): print('ARITMETICA', str(e.op1), str(e.operator), str(e.op2))
        elif isinstance(e, UnaryOperation): print('UNARIA', str(e.val), str(e.op))
        elif isinstance(e, PreOperation): translatePreOperation(e)
        elif isinstance(e, PostOperation): translatePostOperation(e)
        elif isinstance(e, Cast): translateCast(e)
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
    pass

def translateTernaryOperation(exp):
    pass

def translateLogicalOperation(exp):
    pass

def translateBitwiseOperation(exp):
    pass

def translateRelationalOperation(exp):
    pass

def translateShiftOperation(exp):
    pass

def translateArithmeticOperation(exp):
    pass

def translateUnaryOperation(exp):
    pass

def translatePreOperation(exp):
    pass

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
                result.code += var3dName + ' = ' + var3dName + ' + 1' + ';\n'
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


        if(not found): print("No existe la variable")
                
        

        

def translateCast(exp):
    global result
    translateExpressionList(exp.exp)
    result.code += '(' + str(exp.varType) + ')' + str(result.temp) + ';\n'
    pass

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
    print("translating float")
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
        result.code += 'goto ' + cal + ';' + '\n'
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