from .enumTypes import TokenType, STATE, reservedWords, uniqueCharacter, startSimbol
class Token:
    type = 0
    value = 0

    def __init__(self, type=0, value=""):
        self.type = type
        self.value = value

    def __str__(self):
        return str(self.printToken())

    def printToken(self):
        funct = {
            TokenType.ID: lambda: "ID, name="+self.value,
            TokenType.UNUM: lambda: TokenType(self.type).name + ", val="+self.value,
            TokenType.SNUM: lambda: TokenType(self.type).name + ", val="+self.value,
            TokenType.UFLOAT: lambda: TokenType(self.type).name + ", val="+self.value,
            TokenType.SFLOAT: lambda: TokenType(self.type).name + ", val="+self.value,
            TokenType.LT: lambda: self.value,
            TokenType.LOREQ: lambda: self.value,
            TokenType.EQ: lambda: self.value,
            TokenType.BOREQ: lambda: self.value,
            TokenType.BT: lambda: self.value,
            TokenType.DIFF: lambda: self.value,
            TokenType.PLUS: lambda: self.value,
            TokenType.MINUS: lambda: self.value,
            TokenType.MULT: lambda: self.value,
            TokenType.DIV: lambda: self.value,
            TokenType.MOD: lambda: self.value,
            TokenType.INC: lambda: self.value,
            TokenType.DEC: lambda: self.value,
            TokenType.ASSIGN: lambda: self.value,
            TokenType.OPENP: lambda: self.value,
            TokenType.CLOSEP: lambda: self.value,
            TokenType.OPENC: lambda: self.value,
            TokenType.CLOSEC: lambda: self.value,
            TokenType.SEMI: lambda: self.value,
            TokenType.COMMA: lambda: self.value,
            TokenType.MAIN: lambda: "RESERVED WORD: " + self.value,
            TokenType.IF: lambda: "RESERVED WORD: " + self.value,
            TokenType.THEN: lambda: "RESERVED WORD: " + self.value,
            TokenType.ELSE: lambda: "RESERVED WORD: " + self.value,
            TokenType.END: lambda: "RESERVED WORD: " + self.value,
            TokenType.DO: lambda: "RESERVED WORD: " + self.value,
            TokenType.WHILE: lambda: "RESERVED WORD: " + self.value,
            TokenType.CIN: lambda: "RESERVED WORD: " + self.value,
            TokenType.COUT: lambda: "RESERVED WORD: " + self.value,
            TokenType.REAL: lambda: "RESERVED WORD: " + self.value,
            TokenType.INT: lambda: "RESERVED WORD: " + self.value,
            TokenType.BOOLEAN: lambda: "RESERVED WORD: " + self.value,
            TokenType.ERROR: lambda: "ERROR: " + self.value,
            TokenType.EOF: lambda: "EOF"
        }.get(self.type, lambda: "UNKNOWN: token={}, val={}".format(TokenType(self.type).name, self.value))
        return "<"+funct()+">\n"