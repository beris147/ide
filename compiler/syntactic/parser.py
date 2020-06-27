import sys, os
sys.path.append(os.path.relpath("../enumTypes.py"))

from .tree import Tree
from enumTypes import TokenType

def syntaxError(msg, lineo):
    print(f'>>>Syntaxt error at line {lineo} {msg}' )

class Parser:
    def __init__(self, lex):
        self.lex = lex

    def parse(self):
        self.token = self.lex.getToken()
        tree = self.program()
        tree.printPreOrder()
        if self.token.type != TokenType.EOF:
            syntaxError("Code ends before file", self.lex.lineo)
        return tree

    def match(self, expected):
        if self.token.type == expected:
            self.token = self.lex.getToken()
        else:
            syntaxError(f'unexpected token {self.token}', self.lex.lineo)

    # programa → main{ lista-declaración lista-sentencias }
    def program(self):
        t = Tree("program")
        self.match(TokenType.MAIN)
        t.add_child(Tree(TokenType.MAIN))
        self.match(TokenType.OPENC)
        t.add_child(Tree(TokenType.OPENC))
        # statementList()
        # sentencesList()
        self.match(TokenType.CLOSEC)
        return t