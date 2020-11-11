import sys, os, json
sys.path.append(os.path.relpath("../lexic"))

from pathlib import Path
from collections import deque
from lexic.token import Token
from semantic.node import SDT
from semantic.symtab import SymTable

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
        Path(directory+"/compilador").mkdir(parents=True, exist_ok=True)
        with open(directory+"/compilador/tree.json", "w") as fileJSON:
            fileJSON.write(json.dumps(self, default = str, indent = 3))

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