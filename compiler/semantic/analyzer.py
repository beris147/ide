import math

from enumTypes import TokenType
from .symtab import SymTable
from lexic.token import Token
from typing import Callable
from collections import deque 
from collections import namedtuple
from lexic.token import Token
from semantic.node import SDT


class Analyzer:

    def __init__(self, tree) -> None:
        self.tree = tree
        self.symtab = SymTable()
        self.tree.traverse(self.symtab)

def initizalizeStmtList(node, symtab: SymTable):
    if isinstance(node.sdt.data, Token):
        if node.sdt.data.type in [TokenType.INT, TokenType.REAL]:
            node.sdt.type = node.sdt.data.type
        elif node.sdt.data.type == TokenType.ID:
            symtab.insert(node.sdt)
    for child in node.children:
        child.sdt.type = node.sdt.type
        initizalizeStmtList(child, symtab)

def postOrder(root, symtab: SymTable):
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
                        if symtab.lookup(token.value) is not None:
                            symtab.insert(temp.node.sdt)
                            attrs = symtab.getAttr(token.value)
                            temp.node.sdt.type = attrs['type']
                            temp.node.sdt.val = attrs['val']
                            propagate = temp.node.sdt
                        else:
                            #throw error 404
                            pass
                    elif token.type in numeros:
                        temp.node.sdt.type = TokenType.INT if token.type == TokenType.NUM else TokenType.REAL
                        temp.node.sdt.val = int(token.value) if token.type == TokenType.INT else float(token.value) 
                        propagate = temp.node.sdt
                    elif token.type in arithmethicOperators:
                       arithmethicOperations(temp.node, token.type)
                       propagate = temp.node.sdt
                    elif token.type in logicalOperators:
                       relationalOperations(temp.node, token.type)
                       propagate = temp.node.sdt
                    elif token.type == TokenType.ASSIGN:
                        assignOperation(temp.node, symtab)
                elif temp.node.sdt.data in noterminales:
                    temp.node.sdt.type = propagate.type
                    temp.node.sdt.val = propagate.val
                elif temp.node.sdt.data == "SELECT" or temp.node.sdt.data == "ITERATION":
                    checkBooleanExp(temp.node, 1)
                elif temp.node.sdt.data == "REPEAT":
                    checkBooleanExp(temp.node, 3)
                condition = len(Stack)>0 and temp.index == len(Stack[len(Stack)-1].node.children) - 1
            if len(Stack) > 0:
                index = temp.index + 1
                root = Stack[len(Stack)-1].node.children[index]
            else:
                symtab.set_update(True)

def checkBooleanExp(node, pos: int):
    exp = node.children[pos]
    if exp.sdt.type == TokenType.ERROR or exp.sdt.type != TokenType.BOOLEAN:
        #throw error not a boolean expresion in condition if
        node.sdt.type = TokenType.ERROR
        pass

def assignOperation(node, symtab: SymTable):
    #a := b 
    a = node.children[0]
    b = node.children[1]

    if b.sdt.val is None or a.sdt.type == TokenType.ERROR or b.sdt.type == TokenType.ERROR:
        node.sdt.type = TokenType.ERROR
        node.sdt.val = None
        #throw error
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

def arithmethicOperations(node, operation: TokenType):
    # a op b
    a = node.children[0]
    b = node.children[1]

    if a.sdt.val is None or b.sdt.val is None or a.sdt.type == TokenType.ERROR or b.sdt.type == TokenType.ERROR:
        node.sdt.type = TokenType.ERROR
        node.sdt.val = None
        #throw error
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
    node.sdt.type = type
    node.sdt.val = val

def relationalOperations(node, operation: TokenType):
    # a op b
    a = node.children[0]
    b = node.children[1]

    incompatibles = (a.sdt.type == TokenType.BOOLEAN and b.sdt.type != TokenType.BOOLEAN) or (b.sdt.type == TokenType.BOOLEAN and a.sdt.type != TokenType.BOOLEAN)
    if a.sdt.type == TokenType.ERROR or b.sdt.type == TokenType.ERROR or incompatibles or a.sdt.val is None or b.sdt.val is None:
        node.sdt.type = TokenType.ERROR
        node.sdt.val = None
        #throw error
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
    node.sdt.type = type
    node.sdt.val = val

