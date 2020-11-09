from semantic.node import SDT

class SymTable:
    def __init__(self) -> None:
        self.vars = {}

    def lookup(self, name):
        if name in self.vars:
            return self.vars[name]
        else:
            return None

    def insert(self, sdt: SDT):
        name = sdt.data.value

        if name in self.vars:
            self.vars[name]['lines'].append(sdt.data.lineo)
        else:
            self.vars[name] = {'type': sdt.type, 'lines': [sdt.data.lineo], 'val': None}
    
    def setAttr(self, name, attribute, value):
        if name in self.vars:
            if attribute in self.vars[name]:
                self.vars[name][attribute] = value
            else:
                # throw error
                pass
        else:
            # throw error
            pass

    def getAttr(self, name, attribute):
        if name in self.vars:
            if attribute in self.vars[name]:
                return self.vars[name][attribute]
            else:
                # throw error
                pass
        else:
            # throw error
            pass