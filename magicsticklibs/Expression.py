from enum import Enum

# class ArithmeticOperation(Enum):
#     PLUS = 1
#     MINUS = 2
#     MULTIPLY = 3
#     DIVIDE = 4
#     REMAINDER = 5  

# class RelationalOperation(Enum):
#     GREATER = 1
#     LESS = 2
#     GREATER_EQUAL = 3
#     LESS_EQUAL = 4
#     EQUAL = 5
#     NOT_EQUAL = 6

class NumericExpression:
    ''' This is an abstract class '''

class  BinaryExpression(NumericExpression):

    def __init__(self, exp1, exp2, operator):
        self.exp1  = exp1
        self.exp2  = exp2
        self.operator  = operator

class NegativeExpresion(NumericExpression):

    def __init__(self, exp):
        self.exp = exp

class Integer(NumericExpression):

    def __init__(self, val):
        self.val = val

class Float(NumericExpression):

    def __init__(self, val):
        self.val = val
        print('float',val)

class String(NumericExpression):

    def __init__(self, val):
        self.val = val

class Character(NumericExpression):

    def __init__(self, val):
        self.val = val

class Variable(NumericExpression):

    def __init__(self, pointers, id, array, exp):
        self.pointers = pointers
        self.id = id
        self.array = array
        self.exp = exp

class Call(NumericExpression):

    def __init__(self, id, parameters):
        self.id = id
        self.parameters = parameters
