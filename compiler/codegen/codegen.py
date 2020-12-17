import os, sys, random
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
        #if control on stack
        self.ifcounter = 0
        self.ifstack = deque([])
        self.elseif = {}
        #do until control
        self.docounter = 0
        self.dostack = deque([])
        #while control
        self.whilecounter = 0
        self.whilestack = deque([])
        self.whilelevelstack = deque([])
        #sent control stack for conditions
        self.sentstack = deque([])
        
    def run(self):
        for child in self.ast.children:
            if(child.sdt.data == "SENT-LIST"):
                for node in child.children:
                    self.generate(node)
        while(len(self.whilestack) > 0):
            self.close_while()
        self.log("END")
        self.output.close()

    def log(self, line: str) -> None:
        print(line)
        self.output.write(line + '\n')

    def conditional_operation_switch(self, x: TokenType) -> str:
        return {
            TokenType.EQ: 'JNE',
            TokenType.LT: 'JGE',
            TokenType.LOREQ: 'JGR',
            TokenType.BT: 'JLE',
            TokenType.BOREQ: 'JLS',
            TokenType.DIFF: 'JEQ',
        }[x]

    def conditional_label_switch(self, x: TokenType) -> str:
        return {
            TokenType.IF: f'ELSEIF{self.ifstack[len(self.ifstack)-1] if len(self.ifstack) > 0 else 0}',
            TokenType.DO: f'DO{self.dostack[len(self.dostack)-1] if len(self.dostack) > 0 else 0}',
            TokenType.WHILE: f'ENDWHILE{self.whilestack[len(self.whilestack)-1] if len(self.whilestack) > 0 else 0}',
        }[x]

    def instruction_operations(self, token: Token) -> None:
        if token.type == TokenType.ID:
            type = 'float' if self.symtab.getAttr(token.value, 'type') == TokenType.REAL else 'int'
            self.log(f'LOD\t{type}\t{token.value}')
        elif token.type == TokenType.NUM:
            self.log(f'LIT\tint\t{token.value}')
        elif token.type == TokenType.FLOAT:
            self.log(f'LIT\tfloat\t{token.value}')
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

    def conditional_operations(self, token: Token) -> None:
        operation = self.conditional_operation_switch(token.type)
        last_sent = self.sentstack[len(self.sentstack)-1]
        label = self.conditional_label_switch(last_sent)
        self.log(f'{operation}\t{label}')
        self.sentstack.pop()

    def conditional_sentences(self, token: Token, astlevel: int) -> None:
        #if sent
        if token.type == TokenType.IF:
            self.ifcounter = self.ifcounter + 1
            self.ifstack.append(self.ifcounter)
            self.sentstack.append(TokenType.IF)
            self.elseif[self.ifcounter] = False
        elif token.type == TokenType.ELSE:
            topif = self.ifstack[len(self.ifstack)-1]
            self.elseif[topif] = True
            self.log(f'JMP\tENDIF{topif}')
            self.log(f'LAB\tELSEIF{topif}')
        elif token.type == TokenType.END:
            topif = self.ifstack[len(self.ifstack)-1]
            if self.elseif[topif] is False:
                self.log(f'LAB\tELSEIF{topif}')
            self.log(f'LAB\tENDIF{topif}')
            self.ifstack.pop()
            del self.elseif[topif]
        #do until sent
        elif token.type == TokenType.DO:
            self.docounter = self.docounter + 1
            self.dostack.append(self.docounter)
            self.log(f'LAB\tDO{self.docounter}')
            self.sentstack.append(TokenType.DO)
        elif token.type == TokenType.WHILE:
            self.whilecounter = self.whilecounter + 1
            self.whilestack.append(self.whilecounter)
            self.whilelevelstack.append(astlevel)
            self.log(f'LAB\tWHILE{self.whilecounter}')
            self.sentstack.append(TokenType.WHILE)

    def token_operations(self, token: Token, astlevel: int) -> None:
        conditional_tokens = [TokenType.LT, TokenType.LOREQ, TokenType.EQ, TokenType.BOREQ, TokenType.BT, TokenType.DIFF]
        instruction_tokens = [TokenType.ID, TokenType.NUM, TokenType.FLOAT, TokenType.PLUS, TokenType.MINUS, TokenType.MULT, TokenType.DIV, TokenType.MOD, TokenType.ASSIGN, TokenType.INCDECASSIGN]
        conditional_sent_tokens = [TokenType.IF, TokenType.ELSE, TokenType.END, TokenType.DO, TokenType.WHILE]
        if token.type in instruction_tokens:
            self.instruction_operations(token)
        elif token.type in conditional_tokens:
            self.conditional_operations(token)
        elif token.type in conditional_sent_tokens:
            self.conditional_sentences(token, astlevel)

    def close_while(self):
        topwhile = self.whilestack[len(self.whilestack)-1]
        self.log(f'JMP\tWHILE{topwhile}')
        self.log(f'LAB\tENDWHILE{topwhile}')
        self.whilelevelstack.pop()
        self.whilestack.pop()

    def generate(self, root: AST) -> None:
        ASTstack = deque([])
        index = 0
        Pair = namedtuple("Pair", ["node", "index"])
        shouldcout = False
        shouldcin = False
        while root is not None or len(ASTstack) > 0:
            if root is not None:
                ASTstack.append(Pair(root, index))
                index = 0
                root = root.children[0] if len(root.children) >= 1 else None
            else:
                condition = True
                while condition:
                    temp = ASTstack[len(ASTstack)-1]
                    if temp.node.sdt.data == 'SENT':
                        if shouldcout is True:
                            self.log("WRT")
                            shouldcout = False
                        if len(self.whilelevelstack)>0 and len(ASTstack)<self.whilelevelstack[len(self.whilelevelstack)-1]:
                            self.close_while()
                    token = temp.node.sdt.data if isinstance(temp.node.sdt.data, Token) else None
                    if token is not None:
                        if token.type == TokenType.COUT:
                            shouldcout = True
                        elif token.type == TokenType.CIN:
                            shouldcin = True
                        else:
                            self.token_operations(token, len(ASTstack))
                    ASTstack.pop()
                    condition = len(ASTstack)>0 and temp.index == len(ASTstack[len(ASTstack)-1].node.children) - 1
                if len(ASTstack) > 0:
                    index = temp.index + 1
                    root = ASTstack[len(ASTstack)-1].node.children[index]
        if shouldcin:
            self.log("RED")
        