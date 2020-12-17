import os, sys
from pathlib import Path 
from collections import deque, namedtuple
from syntactic.tree import AST
from enumTypes import TokenType
from semantic.symtab import SymTable 
from lexic.token import Token

class CodeGen:
    def __init__(self, directory: str, file: str, ast: AST, symtab: SymTable) -> None:
        self.directory = directory
        self.file = file
        self.ast = ast
        self.symtab = symtab
        Path(directory+"/compilador").mkdir(parents=True, exist_ok=True)
        self.output = open(directory+"/compilador/pcode.o","w+")

        
    def run(self):
        for child in self.ast.children:
            if(child.sdt.data == "SENT-LIST"):
                for node in child.children:
                    self.generate(node)
        self.log("END")
        self.output.close()

    def log(self, line: str) -> None:
        print(line)
        self.output.write(line + '\n')
        
    def generate(self, root: AST) -> None:
        ASTstack = deque([])
        index = 0
        Pair = namedtuple("Pair", ["node", "index"])
        shoudlCout = False
        while root is not None or len(ASTstack) > 0:
            if root is not None:
                ASTstack.append(Pair(root, index))
                index = 0
                root = root.children[0] if len(root.children) >= 1 else None
            else:
                condition = True
                while condition:
                    temp = ASTstack[len(ASTstack)-1]
                    token = temp.node.sdt.data if isinstance(temp.node.sdt.data, Token) else None
                    if token is not None:
                        if token.type == TokenType.ID:
                            self.log("LOD\t" + token.value)
                        elif token.type == TokenType.NUM:
                            self.log("LIT\t" + token.value)
                        #arithmetic operations
                        elif token.type == TokenType.PLUS:
                            self.log("ADD")
                        elif token.type == TokenType.MINUS:
                            self.log("SUB")
                        elif token.type == TokenType.MULT:
                            self.log("MUL")
                        elif token.type == TokenType.DIV:
                            self.log("DIV")
                        elif token.type == TokenType.MOD:
                            self.log("MOD")
                        #assign operation
                        elif token.type == TokenType.ASSIGN:
                            self.log("STO")
                        elif token.type == TokenType.INCDECASSIGN:
                            self.log("STC")
                        #cout
                        elif token.type == TokenType.COUT:
                            #cout the top of the stack when we finish with this sent
                            shoudlCout = True
                    ASTstack.pop()
                    condition = len(ASTstack)>0 and temp.index == len(ASTstack[len(ASTstack)-1].node.children) - 1
                if len(ASTstack) > 0:
                    index = temp.index + 1
                    root = ASTstack[len(ASTstack)-1].node.children[index]
        if shoudlCout is True:
            self.log("WRT")
        