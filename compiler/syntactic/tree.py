import sys, os, math
sys.path.append(os.path.relpath("../lexic"))

from pathlib import Path
from collections import deque 
from collections import namedtuple
from lexic.token import Token
from semantic.node import SDT
from semantic.symtab import SymTable
from enumTypes import TokenType

def printSpaces(Stack):
    print("", end='')
    for _ in range(len(Stack)-1):
        print("\t", end='')

class ATS(dict):
    def __init__(self, sdt = ''):
        super().__init__()
        self.__dict__ = self
        self.sdt = SDT(sdt)
        self.children = []

    def add_child(self, node):
        assert isinstance(node, ATS)
        self.children.append(node)

    def build(self, directory):
        binary = str(self).replace("'", "\"")
        Path(directory+"/compilador").mkdir(parents=True, exist_ok=True)
        with open(directory+"/compilador/tree.json", "w") as fileJSON:
            fileJSON.write(binary)

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

    # TODO: Función a utilizar temporalmente por ahora. Aquí va el switch :v
    def traverse(self, symtab: SymTable) -> None:
        for child in self.children:
            if(child.sdt.data == "STMT-LIST"):
                initizalizeStmtList(child, symtab)
            if(child.sdt.data == "SENT-LIST"):
                for node in child.children:
                    vec = postOrder(node, symtab)
                    print(vec)
        

def initizalizeStmtList(node: ATS, symtab: SymTable):
    if isinstance(node.sdt.data, Token):
        if node.sdt.data.type in [TokenType.INT, TokenType.REAL]:
            node.sdt.type = node.sdt.data.type
        elif node.sdt.data.type == TokenType.ID:
            symtab.insert(node.sdt)
    for child in node.children:
        child.sdt.type = node.sdt.type
        initizalizeStmtList(child, symtab)

def postOrder(root: ATS, symtab: SymTable):
    ans = []
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
                            attrs = symtab.getAttr(token.value)
                            temp.node.sdt.type = attrs['type']
                            temp.node.sdt.val = attrs['val']
                            propagate = temp.node.sdt
                        else:
                            #throw error 404
                            pass
                    elif token.type in numeros:
                        temp.node.sdt.type = TokenType.INT if token.type == TokenType.NUM else TokenType.REAL
                        temp.node.sdt.val = int(token.value) if token.type is TokenType.INT else float(token.value) 
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
                elif(temp.node.sdt.data == "SENT-LIST"):
                    for child in temp.node.children:
                        postOrder(child, symtab)
                ans.append(temp.node.sdt)
                condition = len(Stack)>0 and temp.index == len(Stack[len(Stack)-1].node.children) - 1
            if len(Stack) > 0:
                index = temp.index + 1
                root = Stack[len(Stack)-1].node.children[index]
    return ans


def assignOperation(node: ATS, symtab: SymTable):
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

def arithmethicOperations(node: ATS, operation: TokenType):
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

def relationalOperations(node: ATS, operation: TokenType):
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
        val = a.sdt.val is b.sdt.val
        evaluated = True
    elif operation == TokenType.DIFF:
        val = a.sdt.val is not b.sdt.val
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