from instruction import Instruction
from collections import deque

def isfloat(data):
    try:
        float(data)
        return True
    except ValueError:
        return False

def isint(data):
    try:
        int(data)
        return True
    except ValueError:
        return False

def getvalue(data):
    if isfloat(data) or isint(data):
        return float(data) if "." in data else int(data)
    return data

class CodeStack:
    def __init__(self) -> None:
        self.stack = deque([])
        self.regs = {}
        self.base = 1
        self.counter = 0

    def pop(self):
        a = self.stack[len(self.stack) - 1]
        self.stack.pop()
        return self.regs[a] if isinstance(a, str) else a
    
    def pop_pure(self):
        a = self.stack[len(self.stack) - 1]
        self.stack.pop()
        return a

    #Instructions 
    def lit(self, instruction: Instruction) -> None:
        self.stack.append(instruction.data)
    
    def lod(self, instruction: Instruction) -> None:
        if instruction.data not in self.regs:
            self.regs[instruction.data] = 0
        self.stack.append(instruction.data)

    def sto(self, instruction: Instruction) -> None:
        b = self.pop()
        a = self.pop_pure()
        if isinstance(a, str):
            self.regs[a] = b
        else:
            print("Error storing " + str(instruction.data) + " at " + str(self.counter))

    def stc(self, instruction: Instruction) -> None:
        b = self.pop()
        a = self.pop_pure()
        if isinstance(a, str):
            self.stack.append(self.regs[a])
            self.regs[a] = b
        else:
            print("Error storing " + str(instruction.data) + " at " + str(self.counter))

    def jmp(self, instruction: Instruction) -> None:
        self.counter = instruction.data - 1

    #jump if last two are equal
    def jeq(self, instruction: Instruction) -> None:
        b = self.pop()
        a = self.pop()
        self.counter = instruction.data-1 if a == b else self.counter 
    
    #jump if last two are not equal
    def jne(self, instruction: Instruction) -> None:
        b = self.pop()
        a = self.pop()
        self.counter = instruction.data-1 if a != b else self.counter

    #jump if a < b
    def jls(self, instruction: Instruction) -> None:
        b = self.pop()
        a = self.pop()
        self.counter = instruction.data-1 if a < b else self.counter

    #jump if a <= b
    def jle(self, instruction: Instruction) -> None:
        b = self.pop()
        a = self.pop()
        self.counter = instruction.data-1 if a <= b else self.counter
    
    #jump if a > b
    def jgt(self, instruction: Instruction) -> None:
        b = self.pop()
        a = self.pop()
        self.counter = instruction.data-1 if a > b else self.counter

    #jump if a >= b
    def jge(self, instruction: Instruction) -> None:
        b = self.pop()
        a = self.pop()
        self.counter = instruction.data-1 if a >= b else self.counter

    def wrt(self, instruction: Instruction) -> None:
        a = self.pop()
        print(a)

    #arithmetic operations
    def add(self, instruction: Instruction) -> None:
        b = self.pop()
        a = self.pop()
        self.stack.append(a+b)
    
    def sub(self, instruction: Instruction) -> None:
        b = self.pop()
        a = self.pop()
        self.stack.append(a-b)
    
    def mul(self, instruction: Instruction) -> None:
        b = self.pop()
        a = self.pop()
        self.stack.append(a*b)

    def div(self, instruction: Instruction) -> None:
        b = self.pop()
        a = self.pop()
        res = a/b if "." in str(a) else int(a/b)
        self.stack.append(res)

    def mod(self, instruction: Instruction) -> None:
        b = self.pop()
        a = self.pop()
        self.stack.append(a%b)

    #boolean operations
    def eql(self, instruction: Instruction) -> None:
        b = self.pop()
        a = self.pop()
        self.stack.append(a == b)
    
    def neq(self, instruction: Instruction) -> None:
        b = self.pop()
        a = self.pop()
        self.stack.append(a != b)

    def lss(self, instruction: Instruction) -> None:
        b = self.pop()
        a = self.pop()
        self.stack.append(a < b)

    def leq(self, instruction: Instruction) -> None:
        b = self.pop()
        a = self.pop()
        self.stack.append(a <= b)

    def gtr(self, instruction: Instruction) -> None:
        b = self.pop()
        a = self.pop()
        self.stack.append(a > b)

    def gre(self, instruction: Instruction) -> None:
        b = self.pop()
        a = self.pop()
        self.stack.append(a >= b)