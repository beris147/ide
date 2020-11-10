from semantic.node import SDT
from enumTypes import TokenType

class SymTable(dict):
    def __init__(self) -> None:
        super().__init__()
        self.__dict__ = self
        self.vars = {}
        self.update = True

    def lookup(self, name: str):
        if name in self.vars:
            return self.vars[name]
        else:
            return None

    def set_update(self, val: bool):
        self.update = val

    def insert(self, sdt: SDT):
        name = sdt.data.value

        if name in self.vars:
            self.vars[name]['lines'].append(sdt.data.lineo)
        else:
            self.vars[name] = {'type': sdt.type, 'lines': [sdt.data.lineo], 'val': None}
    
    def setAttr(self, name, attribute, value):
        if self.update:
            if name in self.vars:
                if attribute in self.vars[name]:
                    self.vars[name][attribute] = value
                else:
                    # throw error
                    pass
            else:
                # throw error
                pass

    def getAttr(self, name, attribute = None):
        if name in self.vars:
            if attribute is None:
                val = self.vars[name]['val']
                type = self.vars[name]['type']
                if val is None:
                    return {'type': type, 'val': val}
                if type == TokenType.INT:
                    val = int(val)
                elif type == TokenType.REAL:
                    val = float(val) 
                return {'type': type, 'val': val}
            elif attribute in self.vars[name]:
                if attribute is 'val':
                    type = self.vars[name]['type']
                    val = self.vars[name][attribute]
                    if val is None:
                        return None
                    if type == TokenType.INT:
                        val = int(val)
                    elif type == TokenType.REAL:
                        val = float(val) 
                else:
                    val = self.vars[name]['type']
                return val
            else:
                # throw error
                pass
        else:
            # throw error
            pass