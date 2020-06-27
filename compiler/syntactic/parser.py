from .tree import Tree

class Parser:
    def __init__(self, lex, TokenType):
        self.lex = lex
        self.TokenType = TokenType
        self.tree = Tree()
    
    def parse(self):
        token = self.lex.getToken()
        print(token == self.TokenType.EOF)
        print("Syntax Error, code ends before file!")