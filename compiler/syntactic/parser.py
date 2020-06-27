import sys, os
sys.path.append(os.path.relpath("../enumTypes.py"))

from .tree import Tree
from enumTypes import TokenType

def syntaxError(msg, lineo):
    print("\n>>>")
    print(f'Syntaxt error at line {lineo} {msg}' )

class Parser:
    def __init__(self, lex):
        self.lex = lex

    def parse(self):
        self.token = self.lex.getToken()
        t = self.program()
        if self.token.type != TokenType.EOF:
            print("Code ends before file")
        return t

    def match(self, expected):
        if self.token.type == expected:
            self.token = self.lex.getToken()
        else:
            syntaxError(f'unexpected token {self.token}', self.lex.lineo)

    # programa → main{ lista-declaración lista-sentencias }
    def program(self):
        t = Tree()
        self.match(TokenType.MAIN)
        self.match(TokenType.OPENC)
        # statementList()
        # sentencesList()
        self.match(TokenType.CLOSEC)
        return t