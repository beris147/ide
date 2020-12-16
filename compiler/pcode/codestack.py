from instruction import Instruction

class CodeStack:
    def __init__(self) -> None:
        self.stack = [None]*2048
        self.base = 1
        self.top = 0
        self.counter = 0

    #Instructions 
    def lit(self, instruction: Instruction) -> None:
        self.top = self.top + 1
        self.stack[self.top] = instruction.data
    
    def lod(self, instruction: Instruction) -> None:
        self.top = self.top + 1
        loc = self.getBase(instruction.level) + instruction.data
        self.stack[self.top] = self.stack[loc]

    def sto(self, instruction: Instruction) -> None:
        loc = self.getBase(instruction.level) + instruction.data
        self.stack[loc] = self.stack[self.top]
        self.top = self.top - 1

    def stc(self, instruction: Instruction) -> None:
        loc = self.getBase(instruction.level) + instruction.data
        self.stack[loc] = self.stack[self.top]

    def cal(self, instruction: Instruction) -> None:
        self.stack[self.top+1] = self.getBase(instruction.level)
        self.stack[self.top+2] = self.base
        self.stack[self.top+3] = self.counter
        self.base = self.top+1
        self.counter = instruction.data
    
    def my_int(self, instruction: Instruction) -> None:
        self.top = instruction.data

    def jmp(self, instruction: Instruction) -> None:
        self.counter = instruction.data-1
    
    def jpc(self, instruction: Instruction) -> None:
        if(self.stack[self.top] == 0):
            self.counter = instruction.data - 1
        self.top = self.top - 1

    def wrt(self, instruction: Instruction) -> None:
        loc = self.getBase(instruction.level) + instruction.data
        print(self.stack[loc])
 
    #Operations 
    def rtn(self, instruction: Instruction) -> None:
        self.top = self.base - 1
        self.counter = self.stack[self.top+3]
        self.base = self.stack[self.top+2]
    
    def neg(self, instruction: Instruction) -> None:
        self.stack[self.top] = self.stack[self.top]*-1

    def add(self, instruction: Instruction) -> None:
        self.top = self.top - 1
        self.stack[self.top] += self.stack[self.top+1]
    
    def sub(self, instruction: Instruction) -> None:
        self.top = self.top - 1
        self.stack[self.top] -= self.stack[self.top+1]
    
    def mul(self, instruction: Instruction) -> None:
        self.top = self.top - 1
        self.stack[self.top] *= self.stack[self.top+1]

    def div(self, instruction: Instruction) -> None:
        self.top = self.top - 1
        isint = "." not in str(self.stack[self.top])
        self.stack[self.top] /= self.stack[self.top+1]
        if isint:
            self.stack[self.top] = int(self.stack[self.top])

    def mod(self, instruction: Instruction) -> None:
        self.top = self.top - 1
        self.stack[self.top] %= self.stack[self.top+1]

    def eql(self, instruction: Instruction) -> None:
        self.top = self.top - 1
        self.stack[self.top] = self.stack[self.top] == self.stack[self.top+1]
    
    def neq(self, instruction: Instruction) -> None:
        self.top = self.top - 1
        self.stack[self.top] = self.stack[self.top] != self.stack[self.top+1]

    def lss(self, instruction: Instruction) -> None:
        self.top = self.top - 1
        self.stack[self.top] = self.stack[self.top] < self.stack[self.top+1]

    def leq(self, instruction: Instruction) -> None:
        self.top = self.top - 1
        self.stack[self.top] = self.stack[self.top] <= self.stack[self.top+1]
    
    def gtr(self, instruction: Instruction) -> None:
        self.top = self.top - 1
        self.stack[self.top] = self.stack[self.top] > self.stack[self.top+1]

    def geq(self, instruction: Instruction) -> None:
        self.top = self.top - 1
        self.stack[self.top] = self.stack[self.top] >= self.stack[self.top+1]

    def getBase(self, level) -> int:
        newBase = self.base
        while (level>0):
            newBase = self.stack[newBase]
            level = level - 1
        return newBase