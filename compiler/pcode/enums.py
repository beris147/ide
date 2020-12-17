import enum

class INSCode(enum.Enum): 
    LIT = 1
    OPR = 2
    LOD = 3
    STO = 4
    STC = 40
    CAL = 5
    INT = 6
    JMP = 7
    JEQ = 71
    JNE = 72
    JLS = 73
    JLE = 74
    JGR = 75
    JGE = 76
    WRT = 9
    LAB = 10
    END = 11

    def __repr__(self):
        return str(self.name)

    def __str__(self):
        return str(self.name)

class OPRCode(enum.Enum): 
    RTN = 1
    NEG = 2
    ADD = 3
    SUB = 4
    MUL = 5
    DIV = 6
    ODD = 7
    MOD = 8
    EQL = 9
    NEQ = 10 
    LSS = 11
    LEQ = 12
    GTR = 13
    GEQ = 14

    def __repr__(self):
        return str(self.name)
        
    def __str__(self):
        return str(self.name)