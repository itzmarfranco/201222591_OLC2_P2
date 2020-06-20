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
                sym.tree = symbol.tree
                return
        self.symbols.append(symbol)

    def get(self, id):
        for sym in self.symbols:
            if sym.id == id:
                return sym

    def remove(self, id):
        for sym in self.symbols:
            if sym.id == id:
                self.symbols.remove(sym)
                break


    def print(self):
        print('ID\t', 'TYPE\t', 'VALUE\t', 'LENGTH')
        for sym in self.symbols:
            print(sym.id, '\t', sym.varType, '\t', sym.value, '\t', sym.length)


class Symbol:
    def __init__(self, id, varType, value, length, tree):
        self.id = id
        self.varType = varType
        self.value = value
        self.length = length
        self.tree = tree