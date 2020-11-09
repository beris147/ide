class SymTable:
    def __init__(self) -> None:
        self.vars = {}

    def lookup(self, name):
        if name in self.vars:
            return self.vars[name]
        else:
            return None

    def insert(self, name, type, lineno):
        if name in self.vars:
            self.vars[name]['lines'].append(lineno)
        else:
            self[name] = {'type': type, 'lines': [lineno], 'val': None}
        pass