import math, os

from collections import deque, namedtuple
from pathlib import Path 
from enumTypes import TokenType
from .symtab import SymTable
from lexic.token import Token
from lexic.token import Token
from semantic.node import SDT
from error import Error
from syntactic.tree import CST

class Analyzer:

    def __init__(self, tree: CST, directory: str, traceAnalysis = False) -> None:
        self.tree = tree
        self.symtab = SymTable()
        self.traceAnalysis = traceAnalysis
        Path(directory+"/compilador").mkdir(parents=True, exist_ok=True)
        self.output = open(directory+"/compilador/semantic.o","w+")
        self.lastLineoError = 0

    def semanticError(self, message: str, lineo: int) -> None:
        if self.lastLineoError != lineo: #Avoid spaming errors in the same line
            self.lastLineoError = lineo
            error = Error('Semantic', message, lineo)
            self.output.write(repr(error) + '\n')
            if self.traceAnalysis:
                print(error)
    
    def analyze(self) -> None:
        for child in self.tree.children:
            if(child.sdt.data == "STMT-LIST"):
                self.initizalizeStmtList(child, self.symtab)
            if(child.sdt.data == "SENT-LIST"):
                for node in child.children:
                    self.postOrder(node, self.symtab)
        if self.traceAnalysis:
            print(self.symtab)
        self.output.close()
        return self.tree

    def initizalizeStmtList(self, node: CST, symtab: SymTable):
        if isinstance(node.sdt.data, Token):
            if node.sdt.data.type in [TokenType.INT, TokenType.REAL]:
                node.sdt.type = node.sdt.data.type
            elif node.sdt.data.type == TokenType.ID:
                # TODO: throw error -> redeclarate
                if symtab.insert(node.sdt) is False:
                    node.sdt.type = TokenType.ERROR

        for child in node.children:
            child.sdt.type = node.sdt.type
            self.initizalizeStmtList(child, symtab)

    def postOrder(self, root: CST, symtab: SymTable):
        Stack = deque([])
        index = 0
        Pair = namedtuple("Pair", ["node", "index"])
        propagate = SDT()

        numeros = [TokenType.NUM, TokenType.FLOAT]
        noterminales = ["FACTOR", "EXP", "SIMPLE-EXP", "TERM", "RELATION"]
        arithmethicOperators = [TokenType.PLUS, TokenType.MINUS, TokenType.MULT, TokenType.DIV]
        logicalOperators = [TokenType.BT, TokenType.LT, TokenType.BOREQ, TokenType.LOREQ, TokenType.EQ, TokenType.DIFF]

        while root is not None or len(Stack) > 0:
            if root is not None:
                propagate = SDT()
                Stack.append(Pair(root, index))
                index = 0
                if(root.sdt.data == "SENT-LIST"):
                    symtab.set_update(False)
                root = root.children[0] if len(root.children) >= 1 else None
            else:
                condition = True
                while condition:
                    temp = Stack[len(Stack)-1] 
                    Stack.pop()
                    if isinstance(temp.node.sdt.data, Token):
                        token = temp.node.sdt.data
                        if token.type == TokenType.ID:
                            if symtab.lookup(token.value):
                                symtab.addLine(temp.node.sdt)
                                attrs = symtab.getAttr(token.value)
                                updateSDT(propagate, attrs['type'], attrs['val'], token.lineo, token)
                                updateSDT(temp.node.sdt, propagate.type, propagate.val, propagate.lineo, token)
                            else:
                                self.semanticError(f'{token} is not declared', token.lineo)
                        elif token.type in numeros:
                            propagate.type = TokenType.INT if token.type == TokenType.NUM else TokenType.REAL
                            propagate.val = int(token.value) if token.type == TokenType.NUM else float(token.value) 
                            propagate.lineo = token.lineo
                            updateSDT(temp.node.sdt, propagate.type, propagate.val, propagate.lineo, token)
                        elif token.type in arithmethicOperators:
                            self.arithmethicOperations(temp.node, token.type)
                            propagate = temp.node.sdt
                        elif token.type in logicalOperators:
                            self.relationalOperations(temp.node, token.type)
                            propagate = temp.node.sdt
                        elif token.type == TokenType.ASSIGN:
                            self.assignOperation(temp.node, symtab)
                        elif token.type == TokenType.INCDECASSIGN:
                            self.incdecAssignOperation(temp.node, symtab)
                    elif temp.node.sdt.data in noterminales:
                        updateSDT(temp.node.sdt, propagate.type, propagate.val, propagate.lineo, token)
                    elif temp.node.sdt.data == "SELECT" or temp.node.sdt.data == "ITERATION":
                        self.checkBooleanExp(temp.node, 1)
                    elif temp.node.sdt.data == "REPEAT":
                        self.checkBooleanExp(temp.node, 3)
                    condition = len(Stack)>0 and temp.index == len(Stack[len(Stack)-1].node.children) - 1
                if len(Stack) > 0:
                    index = temp.index + 1
                    root = Stack[len(Stack)-1].node.children[index]
                else:
                    symtab.set_update(True)

    def checkBooleanExp(self, node: CST, pos: int):
        exp = node.children[pos]
        if exp.sdt.type == TokenType.ERROR or exp.sdt.type != TokenType.BOOLEAN:
            self.semanticError(f'incompatible types {exp.sdt.type} cannot be converted to boolean', exp.sdt.lineo)
            updateSDT(node.sdt, TokenType.ERROR)

    def assignOperation(self, node: CST, symtab: SymTable):
        #a := b 
        a = node.children[0]
        b = node.children[1]

        if b.sdt.val is None or a.sdt.type == TokenType.ERROR or b.sdt.type == TokenType.ERROR:
            if b.sdt.val is None: #TODO: find the variable
                if symtab.lookup(b.sdt.token.value):
                    self.semanticError(f'{b.sdt.token} variable is not initialized', b.sdt.lineo)
            updateSDT(node.sdt, TokenType.ERROR, None)
            return

        if a.sdt.type == b.sdt.type:
            val = math.floor(b.sdt.val) if a.sdt.type == TokenType.INT else b.sdt.val
            symtab.setAttr(a.sdt.data.value, "val", val)
        elif a.sdt.type == TokenType.REAL:
            symtab.setAttr(a.sdt.data.value, "val", b.sdt.val*1.0)
        elif a.sdt.type == TokenType.INT:
            symtab.setAttr(a.sdt.data.value, "val", math.floor(b.sdt.val))
        else:
            # throw error incopatible type variable
            pass

    def incdecAssignOperation(self, node: CST, symtab: SymTable):
        #a := a + 1
        a = node.children[0]
        self.assignOperation(node, symtab)
        symtab.removeLine(a.sdt)


    def arithmethicOperations(self, node: CST, operation: TokenType):
        # a op b
        a = node.children[0]
        b = node.children[1]

        if a.sdt.val is None or b.sdt.val is None:
            token = a.sdt.token if a.sdt.val is None else b.sdt.token
            self.semanticError(f'{token} variable is not initialized', token.lineo)
            updateSDT(node.sdt, TokenType.ERROR, None, token.lineo, token)
            return
        if a.sdt.type == TokenType.ERROR or b.sdt.type == TokenType.ERROR:
            updateSDT(node.sdt, TokenType.ERROR, None)
            return

        val = 0
        type = a.sdt.type if a.sdt.type == b.sdt.type else TokenType.REAL if a.sdt.type == TokenType.REAL or b.sdt.type == TokenType.REAL else TokenType.INT
        if operation == TokenType.PLUS:
            val = a.sdt.val + b.sdt.val
        elif operation == TokenType.MINUS:
            val = a.sdt.val - b.sdt.val
        elif operation == TokenType.MULT:
            val = a.sdt.val * b.sdt.val
        elif operation == TokenType.DIV:
            val = a.sdt.val / b.sdt.val
        elif operation == TokenType.MOD:
            val = a.sdt.val % b.sdt.val
        updateSDT(node.sdt, type, val, a.sdt.lineo)

    def relationalOperations(self, node: CST, operation: TokenType):
        # a op b
        a = node.children[0]
        b = node.children[1]

        incompatibles = (a.sdt.type == TokenType.BOOLEAN and b.sdt.type != TokenType.BOOLEAN) or (b.sdt.type == TokenType.BOOLEAN and a.sdt.type != TokenType.BOOLEAN)
        if a.sdt.type == TokenType.ERROR or b.sdt.type == TokenType.ERROR or incompatibles or a.sdt.val is None or b.sdt.val is None:
            if incompatibles: 
                self.semanticError(f'tokens {a.sdt.token} and {b.sdt.token} are not compatibles for a boolean comparation', a.sdt.lineo)
            if a.sdt.val is not None and b.sdt.val is not None:
                self.semanticError('error in expression', a.sdt.lineo)
                updateSDT(node.sdt, TokenType.ERROR, None)
            else:
                token = a.sdt.token if a.sdt.val is None else b.sdt.token
                self.semanticError(f'{token} variable is not initialized', token.lineo)
                updateSDT(node.sdt, TokenType.ERROR, None, token.lineo, token)
            return

        booleans = a.sdt.type == TokenType.BOOLEAN
        val = False
        type = TokenType.BOOLEAN

        evaluated = False
        if operation == TokenType.EQ:
            val = a.sdt.val == b.sdt.val
            evaluated = True
        elif operation == TokenType.DIFF:
            val = a.sdt.val != b.sdt.val
            evaluated = True
        if not booleans:
            if operation == TokenType.LT:
                val = a.sdt.val < b.sdt.val
            elif operation == TokenType.BT:
                val = a.sdt.val > b.sdt.val
            elif operation == TokenType.LOREQ:
                val = a.sdt.val <= b.sdt.val
            elif operation == TokenType.BOREQ:
                val = a.sdt.val >= b.sdt.val
        elif not evaluated:
            type = TokenType.ERROR
            val = None
        updateSDT(node.sdt, type, val, a.sdt.lineo)

def updateSDT(sdt: SDT, type = None, val = None, lineo = None, token = None) -> SDT:
    sdt.type = type
    sdt.val = val
    sdt.lineo = lineo
    sdt.token = token
