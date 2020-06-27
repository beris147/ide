import sys, os
sys.path.append(os.path.relpath("../enumTypes.py"))

from .tree import Tree
from enumTypes import TokenType

class Parser:
    def __init__(self, lex):
        self.lex = lex
        self.tree = Tree()
    
    def parse(self):
        token = self.lex.getToken()
        print(token == TokenType.EOF)
        print("Syntax Error, code ends before file!")

    #programa → main{ lista-declaraciónlista-sentencias }
    def program(self):
        print("building tree")