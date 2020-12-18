import sys, os, json
sys.path.append(os.path.relpath("../lexic"))

from pathlib import Path
from collections import deque, namedtuple
from lexic.token import Token
from semantic.node import SDT
from semantic.symtab import SymTable
from enumTypes import TokenType

def printSpaces(Stack):
    print("", end='')
    for _ in range(len(Stack)-1):
        print("\t", end='')

class CST(dict):
    def __init__(self, sdt = ''):
        super().__init__()
        self.__dict__ = self
        self.sdt = SDT(sdt)
        self.children = []

    def add_child(self, node):
        assert isinstance(node, CST)
        self.children.append(node)

    def build(self, directory):
        pass
        """Path(directory+"/compilador").mkdir(parents=True, exist_ok=True)
        with open(directory+"/compilador/tree.json", "w") as fileJSON:
            fileJSON.write(json.dumps(self, default = str, indent = 3))"""

    def printPreOrder(self):
        Stack = deque([])
        Preorder = []
        print(self.sdt)
        Preorder.append(self)
        Brackets = list()
        Stack.append(self)
        while len(Stack)>0:
            flag = 0
            if len((Stack[len(Stack)-1]).children)== 0: 
                Stack.pop() 
            else:
                parent = Stack[len(Stack)-1]
                if parent not in Brackets:
                    Brackets.append(parent)
                    printSpaces(Stack)
                    print("{")
            for i in range(0, len(parent.children)): 
                if parent.children[i] not in Preorder: 
                    flag = 1
                    Stack.append(parent.children[i])
                    printSpaces(Stack)
                    lineo = parent.children[i].sdt.lineo if isinstance(parent.children[i].sdt, Token) else ""
                    print(parent.children[i].sdt, lineo)
                    Preorder.append(parent.children[i]) 
                    break
            if flag == 0:
                printSpaces(Stack)
                print("}")
                Stack.pop()


class AST(dict):
    def __init__(self, sdt: SDT):
        super().__init__()
        self.__dict__ = self
        self.sdt = sdt
        self.children = []

    def build(self, directory):
        Path(directory+"/compilador").mkdir(parents=True, exist_ok=True)
        with open(directory+"/compilador/ast.json", "w") as fileJSON:
            fileJSON.write(json.dumps(self, default = str, indent = 3))

    def add_child(self, node):
        assert isinstance(node, AST)
        self.children.append(node)

def buildFromCST(root: CST) -> AST:
    Stack = deque([])
    index = 0
    Pair = namedtuple("Pair", ["node", "index"])
    node = AST(None)
    ASTStack = deque([])

    numeros = [TokenType.NUM, TokenType.FLOAT]
    noterminales = ["FACTOR", "EXP", "SIMPLE-EXP", "TERM", "RELATION", "SENT-ASSIGN"]
    arithmethicOperators = [TokenType.PLUS, TokenType.MINUS, TokenType.MULT, TokenType.DIV]
    logicalOperators = [TokenType.BT, TokenType.LT, TokenType.BOREQ, TokenType.LOREQ, TokenType.EQ, TokenType.DIFF]

    while root is not None or len(Stack) > 0:
        if root is not None:
            Stack.append(Pair(root, index))
            index = 0
            root = root.children[0] if len(root.children) >= 1 else None
        else:
            condition = True
            while condition:
                temp = Stack[len(Stack)-1] 
                node = AST(temp.node.sdt)
                Stack.pop()
                if isinstance(temp.node.sdt.data, Token):
                    token = temp.node.sdt.data
                    if token.type == TokenType.ID:
                        ASTStack.append(node)
                    elif token.type in numeros:
                        ASTStack.append(node)
                    elif token.type in arithmethicOperators+logicalOperators+[TokenType.ASSIGN, TokenType.INCDECASSIGN]:
                        operator = node
                        b = ASTStack[len(ASTStack)-1]
                        ASTStack.pop()
                        a = ASTStack[len(ASTStack)-1]
                        ASTStack.pop()
                        operator.add_child(a)
                        operator.add_child(b)
                        ASTStack.append(operator)
                    else:
                        childs = len(temp.node.children)
                        auxStack = deque([])
                        for _ in range(childs):
                            auxStack.append(ASTStack[len(ASTStack)-1])
                            ASTStack.pop()
                        while len(auxStack)>0:
                            node.add_child(auxStack[len(auxStack)-1])
                            auxStack.pop()
                        ASTStack.append(node)
                elif temp.node.sdt.data in noterminales:
                    pass
                else:
                    childs = len(temp.node.children)
                    auxStack = deque([])
                    for _ in range(childs):
                        auxStack.append(ASTStack[len(ASTStack)-1])
                        ASTStack.pop()
                    while len(auxStack)>0:
                        node.add_child(auxStack[len(auxStack)-1])
                        auxStack.pop()
                    ASTStack.append(node)
                condition = len(Stack)>0 and temp.index == len(Stack[len(Stack)-1].node.children) - 1
            if len(Stack) > 0:
                index = temp.index + 1
                root = Stack[len(Stack)-1].node.children[index]
    return node