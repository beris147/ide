import sys, os
sys.path.append(os.path.relpath("../lexic"))

from collections import deque 
from lexic.token import Token

def printSpaces(Stack):
    print("", end='')
    for _ in range(len(Stack)-1):
        print("\t", end='')

class Tree:
    def __init__(self, data):
        self.data = data
        self.children = []

    def add_child(self, node):
        assert isinstance(node, Tree)
        self.children.append(node)

    def printPreOrder(self): 
        Stack = deque([]) 
        Preorder = [] 
        print(self.data)
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
                    lineo = parent.children[i].data.lineo if isinstance(parent.children[i].data, Token) else ""
                    print(parent.children[i].data, lineo)
                    Preorder.append(parent.children[i]) 
                    break
            if flag == 0:
                printSpaces(Stack)
                print("}")
                Stack.pop()