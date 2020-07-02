class Table:
    def __init__(self, symbols = []):
        self.symbols = symbols

    def isSymbolInTable(self, id):
        for sym in self.symbols:
            if id == sym.id:
                return True
        return False

    def add(self, symbol):
        for sym in self.symbols:
            if symbol.id == sym.id:
                sym.varType = symbol.varType
                sym.value = symbol.value
                sym.length = symbol.length
                sym.varName = symbol.varName
                return
        self.symbols.append(symbol)

    def get(self, id):
        for sym in self.symbols:
            if sym.id == id:
                return sym
        return None

    def update(self, id, newValue):
        oldSym = self.get(id)
        newSym = Symbol(oldSym.id, oldSym.varType, newValue, oldSym.length, oldSym.varName)
        self.remove(oldSym)
        self.add(newSym)

    def remove(self, id):
        for sym in self.symbols:
            if sym.id == id:
                self.symbols.remove(sym)
                break


    def print(self):
        print('ID\t\t', 'TYPE\t\t', 'VALUE\t\t\t\t\t\t\t\t', 'LENGTH\t\t', 'NAME3D')
        for sym in self.symbols:
            print(sym.id, '\t\t', sym.varType, '\t\t', sym.value, '\t\t\t\t\t\t\t\t', sym.length, '\t\t', sym.varName)
        print('ttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt')


class Symbol:
    def __init__(self, id, varType, value, length, varName):
        self.id = id
        self.varType = varType
        self.value = value
        self.length = length
        self.varName = varName

    def print(self):
        print('ID', '\t\t', 'Vartype', '\t\t', 'Value', '\t\t', 'Length', '\t\t', '3DName')
        print(self.id, '\t\t', self.varType, '\t\t', self.value, '\t\t', self.length, '\t\t', self.varName)