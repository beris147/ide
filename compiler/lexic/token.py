import sys, os
sys.path.append(os.path.relpath("../enumTypes"))

from enumTypes import TokenType, STATE, reservedWords, uniqueCharacter, startSimbol
class Token:
    type = 0
    value = 0

    def __init__(self, type=0, value="", lineo=""):
        self.type = type
        self.value = value
        self.lineo = lineo

    def __str__(self):
        return str(self.printToken())

    def __repr__(self):
        return str(dict(value = str(self.type.name) + " -> " + self.value))

    def printToken(self):
        funct = {
            TokenType.ID: lambda: "ID: "+self.value,
            TokenType.NUM: lambda: TokenType(self.type).name + ": "+self.value,
            TokenType.SNUM: lambda: TokenType(self.type).name + ": "+self.value,
            TokenType.FLOAT: lambda: TokenType(self.type).name + ": "+self.value,
            TokenType.SFLOAT: lambda: TokenType(self.type).name + ": "+self.value,
            TokenType.LT: lambda: TokenType(self.type).name + ": " + self.value,
            TokenType.LOREQ: lambda: TokenType(self.type).name + ": " + self.value,
            TokenType.EQ: lambda: TokenType(self.type).name + ": " + self.value,
            TokenType.BOREQ: lambda: TokenType(self.type).name + ": " + self.value,
            TokenType.BT: lambda: TokenType(self.type).name + ": " + self.value,
            TokenType.DIFF: lambda: TokenType(self.type).name + ": " + self.value,
            TokenType.PLUS: lambda: TokenType(self.type).name + ": " + self.value,
            TokenType.MINUS: lambda: TokenType(self.type).name + ": " + self.value,
            TokenType.MULT: lambda: TokenType(self.type).name + ": " + self.value,
            TokenType.DIV: lambda: TokenType(self.type).name + ": " + self.value,
            TokenType.MOD: lambda: TokenType(self.type).name + ": " + self.value,
            TokenType.INC: lambda: TokenType(self.type).name + ": " + self.value,
            TokenType.DEC: lambda: TokenType(self.type).name + ": " + self.value,
            TokenType.ASSIGN: lambda: TokenType(self.type).name + ": " + self.value,
            TokenType.OPENP: lambda: "PAREN: " + self.value,
            TokenType.CLOSEP: lambda: "PAREN: " + self.value,
            TokenType.OPENC: lambda: "BRACKET: " + self.value,
            TokenType.CLOSEC: lambda: "BRACKET: " + self.value,
            TokenType.SEMI: lambda: TokenType(self.type).name + ": " + self.value,
            TokenType.COMMA: lambda: TokenType(self.type).name + ": " + self.value,
            TokenType.MAIN: lambda: "RESERVED: " + self.value,
            TokenType.IF: lambda: "RESERVED: " + self.value,
            TokenType.THEN: lambda: "RESERVED: " + self.value,
            TokenType.ELSE: lambda: "RESERVED: " + self.value,
            TokenType.END: lambda: "RESERVED WORD: " + self.value,
            TokenType.DO: lambda: "RESERVED: " + self.value,
            TokenType.WHILE: lambda: "RESERVED: " + self.value,
            TokenType.CIN: lambda: "RESERVED: " + self.value,
            TokenType.COUT: lambda: "RESERVED: " + self.value,
            TokenType.REAL: lambda: "RESERVED: " + self.value,
            TokenType.INT: lambda: "RESERVED: " + self.value,
            TokenType.BOOLEAN: lambda: "RESERVED: " + self.value,
            TokenType.ERROR: lambda: "ERROR: " + self.value,
            TokenType.EOF: lambda: "EOF"
        }.get(self.type, lambda: "UNKNOWN: token={}, val={}".format(TokenType(self.type).name, self.value))
        return "<"+funct()+">"