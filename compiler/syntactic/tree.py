from collections import deque 

def printSpaces(Stack):
    for _ in range(len(Stack)-1):
        print("\t", end='')

class Tree:
    def __init__(self, data, lineo = "", nodeKind = None):
        self.data = data
        self.children = []
        self.lineo = lineo

    def add_child(self, node):
        assert isinstance(node, Tree)
        self.children.append(node)

    def printPreOrder(self): 
        Stack = deque([]) 
        Preorder = [] 
        print(self.data, self.lineo)
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
                    print(parent.children[i].data, parent.children[i].lineo)
                    Preorder.append(parent.children[i]) 
                    break
            if flag == 0:
                printSpaces(Stack)
                print("}")
                Stack.pop()