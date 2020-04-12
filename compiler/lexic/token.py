from enumTypes import TokenType, STATE
from variables import file, posinfile

class Token:
    type = 0
    value = 0

    def __init__(self, type=0, value=""):
        self.type = type
        self.value = value

    def __str__(self):
        return str(self.printToken())

    def printToken(self):
        funct = {
            TokenType.ID: lambda: "ID, name="+self.value,
            TokenType.UNUM: lambda: TokenType(self.type).name + ", val: "+self.value,
            TokenType.SNUM: lambda: TokenType(self.type).name + ", val: "+self.value,
            TokenType.UFLOAT: lambda: TokenType(self.type).name + ", val: "+self.value,
            TokenType.SFLOAT: lambda: TokenType(self.type).name + ", val: "+self.value,
            TokenType.LT: lambda: TokenType(self.type).name + ", val: " + self.value,
            TokenType.LOREQ: lambda: TokenType(self.type).name + ", val: " + self.value,
            TokenType.EQ: lambda: TokenType(self.type).name + ", val: " + self.value,
            TokenType.BOREQ: lambda: TokenType(self.type).name + ", val: " + self.value,
            TokenType.BT: lambda: TokenType(self.type).name + ", val: " + self.value,
            TokenType.DIFF: lambda: TokenType(self.type).name + ", val: " + self.value,
            TokenType.PLUS: lambda: self.value,
            TokenType.MINUS: lambda: self.value,
            TokenType.MULT: lambda: self.value,
            TokenType.DIV: lambda: self.value,
            TokenType.MOD: lambda: self.value,
            TokenType.ASSIGN: lambda: TokenType(self.type).name + ", val: " + self.value,
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
    elif c == "-":
        return STATE.MINUS
    elif c == "/":
        return STATE.DIAG
    elif c == "<":
        return STATE.MINOR
    elif c == ">":
        return STATE.BIGGER
    elif c == "=":
        return STATE.EQUAL
    elif c == "!":
        return STATE.NOT
    elif c == ":":
        return STATE.ASSIGN
    elif c == " " or c == "\t" or c == "\n":
        return STATE.SPACES
    return STATE.ERROR

def getToken():
    currentToken = Token()
    state = STATE(0)
    global posinfile
    with open(file) as f:
        f.seek(posinfile)
        while state != STATE.DONE:
            save = True
            ungetChar = False
            c = f.read(1)
            if not c:
                currentToken.type = TokenType.EOF
                state = STATE.DONE
                break

            save = True
            if(state == STATE.START):
                state = checkStart(c)
                if(state == STATE.ERROR or state == STATE.SPACES): #FIXME: STATE.SPACES
                    save = False
                    state = STATE.START
            
            elif(state == STATE.MINOR):
                if(c == '='):
                    currentToken.type = TokenType.LOREQ
                else:
                    save = False
                    ungetChar = True
                    currentToken.type = TokenType.LT
                state = STATE.DONE
            elif(state == STATE.BIGGER):
                if(c == '='):
                    currentToken.type = TokenType.BOREQ
                else:
                    save = False
                    ungetChar = True
                    currentToken.type = TokenType.BT
                state = STATE.DONE

            # == != :=
            elif(state == STATE.EQUAL and c == "="):
                currentToken.type = TokenType.EQ
                state = STATE.DONE
            elif(state == STATE.NOT and c == "="):
                currentToken.type = TokenType.DIFF
                state = STATE.DONE
            elif(state == STATE.ASSIGN and c == "="):
                currentToken.type = TokenType.ASSIGN
                state = STATE.DONE

            if (save == True):
                currentToken.value += c

            posinfile = f.tell()
            if (ungetChar): posinfile -= 1
        f.close()
    return currentToken