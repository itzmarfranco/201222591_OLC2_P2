class Instruction:
    # abstract class
    '''This is an abstract class'''

class printf(Instruction):

    def __init__(self, string, parameters):
        self.string = string
        self.parameters = parameters

class scanf(Instruction):

    def __init__(self, string, parameter):
        self.string = string
        self.parameter = parameter

class definition(Instruction):

    def __init__(self, modifier, type, id_value):
        self.modifier = modifier
        self.sign = type[0][0]
        self.varType = type[0][1] #sign scalar pointers
        self.pointers = type[1]
        self.id_value = id_value
        
        #print(id_value)
        # for i in id:
        #     self.id.append(i)

class declaration(Instruction):

    def __init__(self, modifier, varType, id, value):
        self.modifier = modifier
        self.varType = varType[0][1] #sign scalar pointers
        self.pointers = varType[1]
        self.id = id # var list
        self.value = value

class assignation(Instruction):

    def __init__(self, id, value):
        self.id = id
        self.value = value

class Parameter(Instruction):

    def __init__(self, const, sign, scalar, pointer, id):
        self.const = const
        self.sign = sign
        self.scalar = scalar
        self.pointer = pointer
        self.id = id

class function(Instruction):

    def __init__(self, varType, id, parameters, body):
        print()
        self.sign = varType[0][0]
        self.varType = varType[0][1]
        self.pointers = varType[1]
        self.id = id
        self.parameters = []
        # split parameters
        # ('unconst', (('signed', 'int'), None), 'c')
        # p[0] = 'unconst'
        # p[1] = (('signed', 'int'), None)
            #p[1][0] = ('signed', 'int')
                #p[1][0][0] = 'signed'
                #p[1][0][1] = 'int'
            #p[1][1] = None
        # p[2] = 'c'
        if parameters != None:
            if type(parameters) == tuple and parameters[0] not in ('const', 'unconst'):
                for p in parameters:
                    cn = '' #constant
                    sg = '' #signed
                    sc = '' #scalar
                    pn = None #pointers
                    pr = ''  #id for parameter
                    if p[0] == 'const': cn = 'const'
                    else: cn = None
                    if p[1][0][0] == 'signed': sg = 'signed'
                    else: sg = 'unsigned'
                    #print ('PARAMETERS   ',p)
                    sc = p[1][0][1]
                    pn = p[1][1]
                    pr = p[2]
                    param = Parameter(cn, sg, sc, pn, pr)
                    self.parameters.append(param)
            else:
                cn = '' #constant
                sg = '' #signed
                sc = '' #scalar
                pn = None #pointers
                pr = ''  #id for parameter
                if parameters[0] == 'const': cn = 'const'
                else: cn = None
                if parameters[1][0][0] == 'signed': sg = 'signed'
                else: sg = 'unsigned'
                #print ('PARAMETERS   ',p)
                sc = parameters[1][0][1]
                pn = parameters[1][1]
                pr = parameters[2]
                param = Parameter(cn, sg, sc, pn, pr)
                self.parameters.append(param)
        else:
            self.parameters = None

        self.body = body


class iff(Instruction):

    def __init__(self, condition, statements):
        self.condition = condition
        self.statements = statements

class ifelse(Instruction):

    def __init__(self, condition, statementsTrue, statementsFalse):
        self.condition = condition
        self.statementsTrue = statementsTrue
        self.statementsFalse = statementsFalse

class whilee(Instruction):

    def __init__(self, condition, statements):
        self.condition = condition
        self.statements = statements

class dowhile:

    def __init__(self, condition, statements):
        self.condition = condition
        self.statements = statements

class forr(Instruction):

    def __init__(self, arg1, arg2, arg3, statements):
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3
        self.statements = statements

class Case(Instruction):

    def __init__(self, value, statements):
        self.value = value
        self.statements = statements

class Switch(Instruction):

    def __init__(self, condition, cases):
        self.condition = condition
        reversed_list = cases[::-1]
        self.cases = reversed_list

class enum(Instruction):
    
    def __init__(self, id, elements):
        self.id = id
        self.elements = elements

class struct(Instruction):
    
    def __init__(self, id, vars):
        self.id = id
        self.vars = vars

class union(Instruction):

    def __init__(self, id, vars):
        self.id = id
        self.vars = vars

class Cast(Instruction):
    # cast
    def __init__(self, varType, exp):
        self.varType = varType[0][1]
        self.exp = exp

class Return():

    def __init__(self, ret):
        self.ret = ret

class Break(Instruction):

    def __init__(self, ret):
        self.ret = ret

class Continue(Instruction):

    def __init__(self, ret):
        self.ret = ret

class Goto(Instruction):

    def __init__(self, ret):
        self.ret = ret

class Label(Instruction):

    def __init__(self, label):
        self.label = label

class PostOperation(Instruction):

    def __init__(self, val, op):
        self.val = val
        self.op = op

class PreOperation(Instruction):

    def __init__(self, val, op):
        self.val = val
        self.op = op

class UnaryOperation(Instruction):

    def __init__(self, val, op):
        self.val = val
        self.op = op

class ArithmeticOperation(Instruction):
    # + - * / % 
    def __init__(self,  op1, op2, operator):
        self.op1 = op1
        self.op2 = op2
        self.operator = operator

class ShiftOperation(Instruction):
    # >> <<
    def __init__(self, op1, op2, operator):
        self.op1 = op1
        self.op2 = op2
        self.operator = operator

class RelationalOperation(Instruction):
    # > < >= <= == !=
    def __init__(self, op1, op2, operator):
        self.op1 = op1
        self.op2 = op2
        self.operator = operator

class LogicalOperation(Instruction):
    # && ||
    def __init__(self, op1, op2, operator):
        self.op1 = op1
        self.op2 = op2
        self.operator = operator

class BitwiseOperation(Instruction):
    # & | ^
    def __init__(self, op1, op2, operator):
        self.op1 = op1
        self.op2 = op2
        self.operator = operator

class TernaryOperation(Instruction):
    # a?b:c
    def __init__(self, op1, op2, op3):
        self.op1 = op1
        self.op2 = op2
        self.op3 = op3

class AssignOperation(Instruction):
    # = += -= *= /= ^= &= |= <<= >>=
    def __init__(self, op1, op2, operator):
        self.op1 = op1
        self.op2 = op2
        self.operator = operator

class ExpresionList():

    def __init__(self, expressions):
        self.expressions = expressions