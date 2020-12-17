from enums import INSCode, OPRCode
from instruction import Instruction
from codestack import CodeStack, getvalue

class Machine:
    def __init__(self, file: str) -> None:
        self.file = file

    def readfile(self):
        return (ln + '\n' for ln in open(self.file, 'r'))

    def run(self) -> None:
        instructions = []
        for line in list(self.readfile()):
            parts = line.split('\t')
            if len(parts) > 2:
                print("Error with " + line)
                break
            operation = parts[0].split('\n')[0]
            data = getvalue(parts[1].split('\n')[0]) if len(parts) > 1 else None
            instruction = Instruction(operation, data)
            instructions.append(instruction)
            if operation == INSCode.END.name:
                break
        print("Starting p-code execution...")
        codeStack = CodeStack()
        i = 0
        while i < len(instructions) and instructions[i].operation != INSCode.END.name:
            instruction = instructions[i]
            executeInstruction(instruction, codeStack)
            i = codeStack.counter

def executeInstruction(instruction: Instruction, codeStack: CodeStack) -> None:
    codeStack.counter = codeStack.counter + 1
    func = {
        #instructions
        INSCode.LIT.name: lambda: codeStack.lit(instruction),
        INSCode.LOD.name: lambda: codeStack.lod(instruction),
        INSCode.STO.name: lambda: codeStack.sto(instruction),
        INSCode.STC.name: lambda: codeStack.stc(instruction),
        #jumps instructions
        INSCode.JMP.name: lambda: codeStack.jmp(instruction),
        INSCode.JEQ.name: lambda: codeStack.jeq(instruction),
        INSCode.JNE.name: lambda: codeStack.jne(instruction),
        INSCode.JLS.name: lambda: codeStack.jls(instruction),
        INSCode.JLE.name: lambda: codeStack.jle(instruction),
        INSCode.JGR.name: lambda: codeStack.jgr(instruction),
        INSCode.JGE.name: lambda: codeStack.jge(instruction),
        #cout
        INSCode.WRT.name: lambda: codeStack.wrt(instruction),
        #arithmetic operations
        OPRCode.ADD.name: lambda: codeStack.add(instruction),
        OPRCode.SUB.name: lambda: codeStack.sub(instruction),
        OPRCode.MUL.name: lambda: codeStack.mul(instruction),
        OPRCode.DIV.name: lambda: codeStack.div(instruction),
        OPRCode.MOD.name: lambda: codeStack.mod(instruction),
        #boolean operations
        OPRCode.EQL.name: lambda: codeStack.eql(instruction),
        OPRCode.NEQ.name: lambda: codeStack.neg(instruction),
        OPRCode.LSS.name: lambda: codeStack.lss(instruction),
        OPRCode.LEQ.name: lambda: codeStack.leq(instruction),
        OPRCode.GTR.name: lambda: codeStack.gtr(instruction),
        OPRCode.GEQ.name: lambda: codeStack.geq(instruction)
    }.get(instruction.operation,lambda : print('Invalid'))
    func()