from enumTypes import TokenType
import sys, os
sys.path.append(os.path.relpath("../lexic"))

from pathlib import Path
from collections import deque 
from collections import namedtuple
from lexic.token import Token
from semantic.node import SDT
from semantic.symtab import SymTable

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
                    vec = postOrder(node, SymTable)
                    print(vec)

def initizalizeStmtList(node: ATS, symtab: SymTable):
    if isinstance(node.sdt.data, Token):
        if node.sdt.data.type in [TokenType.INT, TokenType.REAL, TokenType.BOOLEAN]:
            node.sdt.type = node.sdt.data.type
        elif node.sdt.data.type == TokenType.ID:
            symtab.insert(node.sdt)
    for child in node.children:
        child.sdt.type = node.sdt.type
        initizalizeStmtList(child, symtab)


def postOrder(node: ATS, symtab: SymTable):
    ans = []
    Stack = deque([])
    index = 0
    Pair = namedtuple("Pair", ["node", "index"])
    while node is not None or len(Stack) > 0:
        if node is not None: #Si es no None aun tenemos nodos a la izquierda
            Stack.append(Pair(node, index))
            index = 0
            node = node.children[0] if len(node.children) >= 1 else None
        else: # Si llegamos al final de la izquierda vaciamos los que esten al nivel
            condition = True
            while condition:
                temp = Stack[len(Stack)-1] 
                Stack.pop()
                # Los que vamos sacando son los hijos, de momento los meto a la lista para tenerlos en 
                # el orden que van saliendo, de aqui podemos comprobar si un nodo es terminal, si llega a 
                # ser un ID hay que buscarlo en la tabla de simbolos, si es reservado no se hace nada
                # si es un intermedio toma los valores que tiene su primer hijo. 
                # Los operadores hacen otras cosas
                ans.append(temp.node.sdt)
                condition = len(Stack)>0 and temp.index == len(Stack[len(Stack)-1].node.children) - 1
            if len(Stack) > 0:
                index = temp.index + 1
                node = Stack[len(Stack)-1].node.children[index]
    return ans