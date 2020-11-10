from semantic.node import SDT
from enumTypes import TokenType

class SymTable(dict):
    def __init__(self) -> None:
        super().__init__()
        self.__dict__ = self
        self.vars = {}
        self.update = True

    # Determinates if symtable saves new values
    def set_update(self, val: bool):
        self.update = val

    # Searches the var in symtable
    def lookup(self, name: str) -> bool:
        return name in self.vars

    # Inserts the var in symtable. Returns False if the var doesn't exist 
    def insert(self, sdt: SDT) -> bool:
        name = sdt.data.value
        if name not in self.vars:
            self.vars[name] = {'type': sdt.type, 'lines': [sdt.data.lineo], 'val': None}
            return True
        else:
            return False

    # Adds the line of present var
    def addLine(self, sdt: SDT):
        name = sdt.data.value
        assert name in self.vars
        # Add line
        self.vars[name]['lines'].append(sdt.data.lineo)

    # Remove the line of present var
    def removeLine(self, sdt: SDT):
        name = sdt.data.value
        assert name in self.vars
        # Add line
        self.vars[name]['lines'].remove(sdt.data.lineo)

    # Sets the value of a var's attribute
    def setAttr(self, name, attribute, value):
        if self.update:
            assert name in self.vars
            # Checks if the attribute exists
            if attribute in self.vars[name]:
                self.vars[name][attribute] = value
            else:
                # throw local error
                pass

    # Gets all attributes or the given one.
    def getAttr(self, name, attribute = None):
        assert name in self.vars
        # Checks if attribute has value
        if attribute is None:
            return {'type': self.vars[name]['type'], 'val': self.vars[name]['val']}
        elif attribute in self.vars[name]:
            return self.vars[name][attribute]