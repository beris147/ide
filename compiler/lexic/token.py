from enumTypes import TokenType, STATE
from variables import file, posinfile

class Token:
      type = 0
      value = 0
      def __init__(self, type = 0, value=""):
            self.type = type
            self.value = value
      def printToken(self):
            funct = {
                TokenType.ID: lambda: "ID, name="+self.value,
                TokenType.UNUM: lambda: TokenType(self.type).name + ", val="+self.value,
                TokenType.SNUM: lambda: TokenType(self.type).name + ", val="+self.value,
                TokenType.UFLOAT: lambda: TokenType(self.type).name + ", val="+self.value,
                TokenType.SFLOAT: lambda: TokenType(self.type).name + ", val="+self.value,
                TokenType.LT: lambda: self.value,
                TokenType.LOREQ: lambda: self.value,
                TokenType.EQ: lambda: self.value,
                TokenType.BOREQ: lambda: self.value,
                TokenType.BT: lambda: self.value,
                TokenType.DIFF: lambda: self.value,
                TokenType.PLUS: lambda: self.value,
                TokenType.MINUS: lambda: self.value,
                TokenType.MULT: lambda: self.value,
                TokenType.DIV: lambda: self.value,
                TokenType.MOD: lambda: self.value,
                TokenType.ASSIGN: lambda: self.value,
                TokenType.IF: lambda: "RESERVED: " + self.value,
                TokenType.ELSE: lambda: "RESERVED: " + self.value,
                TokenType.EOF: lambda: "EOF"
              }.get(self.type, lambda: "UNKNOWN: token={}, val={}".format(self.type, self.value))
            return funct()

def checkStart(c):
    if c.isdigit():
        return STATE.NUM
    elif c.isalpha():
        return STATE.ID
    elif c == "+":
        return STATE.PLUS
    return STATE.ERROR

def getToken():
    currentToken = Token()
    state = STATE(0)
    global posinfile
    with open(file) as f:
        f.seek(posinfile)
        while state != STATE.DONE:
            save = True
            c = f.read(1)
            if not c:
                currentToken.type = TokenType.EOF
                state = STATE.DONE
                break
            #if(state == STATE.START):
                #state = checkStart(c)
            print(c, end = '')
            posinfile = f.tell()
        f.close()
    return currentToken