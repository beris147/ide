from enums import INSCode, OPRCode
from instruction import Instruction
from codestack import CodeStack

class Machine:
    def __init__(self, file: str) -> None:
        self.file = file

    def readfile(self):
        return (ln + '\n' for ln in open(self.file, 'r'))

    def run(self) -> None:
        instructions = []
        for line in list(self.readfile()):
            parts = line.split('\t')
            if len(parts) != 3:
                print("Error with " + line)
                break
            operation = parts[0]
            level = parts[1]
            data = parts[2]
            if isint(level) == False or (isint(data) == False and isfloat(data) == False):
                print("Error with " + line)
                break
            level = int(level)
            data = float(data) if "." in data else int(data)
            if operation == INSCode.END.name:
                break
            instruction = Instruction(operation, level, data)
            instructions.append(instruction)

        print("Starting p-code execution...")
        codeStack = CodeStack()
        for instruction in instructions:
            executeInstruction(instruction, codeStack)


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

def executeInstruction(instruction: Instruction, codeStack: CodeStack) -> None:
    codeStack.counter = codeStack.counter + 1
    func = {
        INSCode.LIT.name: lambda: codeStack.lit(instruction),
        INSCode.LOD.name: lambda: codeStack.lod(instruction),
        INSCode.STO.name: lambda: codeStack.sto(instruction),
        INSCode.STC.name: lambda: codeStack.stc(instruction),
        INSCode.CAL.name: lambda: codeStack.cal(instruction),
        INSCode.INT.name: lambda: codeStack.my_int(instruction),
        INSCode.JMP.name: lambda: codeStack.jmp(instruction),
        INSCode.JPC.name: lambda: codeStack.jpc(instruction),
        INSCode.WRT.name: lambda: codeStack.wrt(instruction),
        OPRCode.RTN.name: lambda: codeStack.rtn(instruction),
        OPRCode.NEG.name: lambda: codeStack.neg(instruction),
        OPRCode.ADD.name: lambda: codeStack.add(instruction),
        OPRCode.SUB.name: lambda: codeStack.sub(instruction),
        OPRCode.MUL.name: lambda: codeStack.mul(instruction),
        OPRCode.DIV.name: lambda: codeStack.div(instruction),
        OPRCode.MOD.name: lambda: codeStack.mod(instruction),
        OPRCode.EQL.name: lambda: codeStack.eql(instruction),
        OPRCode.NEQ.name: lambda: codeStack.neg(instruction),
        OPRCode.LSS.name: lambda: codeStack.lss(instruction),
        OPRCode.LEQ.name: lambda: codeStack.leq(instruction),
        OPRCode.GTR.name: lambda: codeStack.gtr(instruction),
        OPRCode.GEQ.name: lambda: codeStack.geq(instruction)
    }.get(instruction.operation,lambda : print('Invalid'))
    func()