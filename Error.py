class Error:
    def __init__(self, value, line, column):
        self.value = value
        self.line = line
        self.column = column


class ErrorList:
    def __init__(self, errors = []):
        self.errors = errors

    def add(self, error):
        self.errors.append(error)

    def clear(self):
        self.errors.clear()

    def print(self):
        for e in  self.errors:
            print(e.value, '. Line:', e.line, '. Column:', e.column)