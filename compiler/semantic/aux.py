import math

from collections import deque, namedtuple
from enumTypes import TokenType
from .symtab import SymTable
from lexic.token import Token
from lexic.token import Token
from semantic.node import SDT
from error import Error
class AST(dict):
    def __init__(self, token: Token, value = None, childs = []):
        super().__init__()
        self.__dict__ = self
        self.token = token
        self.value = value
        self.childs = childs

    def add_child(self, node):
        assert isinstance(node, AST)
        self.childs.append(node)

def makeAst(root, symtab: SymTable) -> AST:
    Stack = deque([])
    index = 0
    Pair = namedtuple("Pair", ["node", "index"])
    astList = []

    numeros = [TokenType.NUM, TokenType.FLOAT]
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
                        if symtab.lookup(token.value):
                            symtab.addLine(temp.node.sdt)
                            attrs = symtab.getAttr(token.value)
                            astList.append(AST(token, attrs['val']))
                        else:
                            #semanticError(f'{token} is not declared', token.lineo)
                            pass
                    elif token.type in numeros:
                        astList.append(AST(token,  int(token.value) if token.type == TokenType.NUM else float(token.value)))
                    elif token.type in arithmethicOperators or token.type in logicalOperators or token.type in [TokenType.ASSIGN]:
                        astList.append(AST(token))
                condition = len(Stack)>0 and temp.index == len(Stack[len(Stack)-1].node.children) - 1
            if len(Stack) > 0:
                index = temp.index + 1
                root = Stack[len(Stack)-1].node.children[index]
            else:
                symtab.set_update(True)
    
    nodes = deque([])
    print(astList)
    for node in astList:
        if node.token.type in numeros or node.token.type == TokenType.ID:
            nodes.append(node)
        elif node.token.type in arithmethicOperators or node.token.type in  logicalOperators or node.token.type in [TokenType.ASSIGN]:
            b = nodes[len(nodes)-1]
            nodes.pop()
            a = nodes[len(nodes)-1]
            nodes.pop()
            node.add_child(a)
            node.add_child(b)
            nodes.append(node)

    while len(nodes) > 1:
        parent = nodes[len(nodes)-1]
        nodes.pop()
        b = nodes[len(nodes)-1]
        nodes.pop()
        a = nodes[len(nodes)-1]
        nodes.pop()
        parent.add_child(a)
        parent.add_child(b)

    return nodes[len(nodes)-1]