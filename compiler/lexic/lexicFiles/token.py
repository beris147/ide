from .enumTypes import TokenType, STATE, reservedWords, uniqueCharacter, startSimbol
#import lexicFiles.variables as var delete
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
            TokenType.INC: lambda: self.value,
            TokenType.DEC: lambda: self.value,
            TokenType.ASSIGN: lambda: self.value,
            TokenType.OPENP: lambda: self.value,
            TokenType.CLOSEP: lambda: self.value,
            TokenType.OPENC: lambda: self.value,
            TokenType.CLOSEC: lambda: self.value,
            TokenType.SEMI: lambda: self.value,
            TokenType.COMMA: lambda: self.value,
            TokenType.MAIN: lambda: "RESERVED WORD: " + self.value,
            TokenType.IF: lambda: "RESERVED WORD: " + self.value,
            TokenType.THEN: lambda: "RESERVED WORD: " + self.value,
            TokenType.ELSE: lambda: "RESERVED WORD: " + self.value,
            TokenType.END: lambda: "RESERVED WORD: " + self.value,
            TokenType.DO: lambda: "RESERVED WORD: " + self.value,
            TokenType.WHILE: lambda: "RESERVED WORD: " + self.value,
            TokenType.CIN: lambda: "RESERVED WORD: " + self.value,
            TokenType.COUT: lambda: "RESERVED WORD: " + self.value,
            TokenType.REAL: lambda: "RESERVED WORD: " + self.value,
            TokenType.INT: lambda: "RESERVED WORD: " + self.value,
            TokenType.BOOLEAN: lambda: "RESERVED WORD: " + self.value,
            TokenType.ERROR: lambda: "ERROR: " + self.value,
            TokenType.EOF: lambda: "EOF"
        }.get(self.type, lambda: "UNKNOWN: token={}, val={}".format(TokenType(self.type).name, self.value))
        return "<"+funct()+">\n"
""" MOVED TO LEXICMAIN, delete
def reservedLookUp(value):
    resWord = reservedWords.get(value)
    return resWord if resWord else TokenType.ID

def uniqueLookUp(c):
    unique = uniqueCharacter.get(c)
    return unique if unique else TokenType.ERROR

def checkStart(c):
    if c.isdigit():
        return STATE.NUM
    elif c.isalpha():
        return STATE.ID
    else:
        simbol = startSimbol.get(c)
        return simbol if simbol else STATE.UNIQUE

def getToken():
    currentToken = Token()
    state = STATE(0)
    with open(var.file) as f:
        f.seek(var.posinfile)
        while state != STATE.DONE:
            save = True
            ungetChar = False
            c = f.read(1)
            if state == STATE.START:
                if not c:
                    currentToken.type = TokenType.EOF
                    state = STATE.DONE
                    break
                state = checkStart(c)
                if state == STATE.SPACES:
                    state = STATE.START
                    if(c == '\n'):
                        var.lineo = var.lineo + 1
                    continue
                # Unique character
                elif state == STATE.UNIQUE:
                    state = STATE.DONE
                    currentToken.type = uniqueLookUp(c)
            # Identifiers
            else:
                if state == STATE.ID:
                    if not (c.isalnum() or c == "_"):
                        save = False
                        ungetChar = True if c else False
                        currentToken.type = TokenType.ID
                        state = STATE.DONE

                # Numbers
                elif state == STATE.NUM:
                    if c == ".":
                        state = STATE.DOT
                    elif not c.isdigit():
                        save = False
                        ungetChar = True if c else False
                        currentToken.type = TokenType.UNUM if currentToken.value[0].isdigit() else TokenType.SNUM
                        state = STATE.DONE                
                # Dot .
                elif state == STATE.DOT:
                    if c.isdigit():
                        state = STATE.FLOAT
                    else:
                        save = False
                        ungetChar = True if c else False
                        currentToken.type = TokenType.ERROR
                        state = STATE.DONE
                # Float numbers
                elif state == STATE.FLOAT:
                    if not c.isdigit():
                        save = False
                        ungetChar = True if c else False
                        currentToken.type = TokenType.UFLOAT if currentToken.value[0].isdigit() else TokenType.SFLOAT
                        state = STATE.DONE

                # +
                elif state == STATE.PLUS:
                    if c.isdigit():
                        state = STATE.NUM
                    elif c == "+":
                        currentToken.type = TokenType.INC
                        state = STATE.DONE
                    else:
                        save = False
                        ungetChar = True if c else False
                        currentToken.type = TokenType.PLUS
                        state = STATE.DONE

                # -
                elif state == STATE.MINUS:
                    if c.isdigit():
                        state = STATE.NUM
                    elif c == "-":
                        currentToken.type = TokenType.DEC
                        state = STATE.DONE
                    else:
                        save = False
                        ungetChar = True if c else False
                        currentToken.type = TokenType.MINUS
                        state = STATE.DONE

                # /
                elif state == STATE.DIAG:
                    if c == "*":
                        state = STATE.COMM_BLOCK
                        currentToken.value = ""
                        continue
                    elif c == "/":
                        state = STATE.COMM_LINE
                        currentToken.value = ""
                        continue
                    else:
                        save = False
                        ungetChar = True if c else False
                        currentToken.type = TokenType.DIV
                        state = STATE.DONE

                # /* Comment block
                elif state == STATE.COMM_BLOCK:
                    if c == "*":
                        state = STATE.COMM_BLOCK_END
                    elif c == "\n":
                        var.lineo += 1
                    continue
                # */ Comment block end
                elif state == STATE.COMM_BLOCK_END:
                    if c == "/":
                        state = STATE.START
                    elif c != "*":
                        state = STATE.COMM_BLOCK
                    elif c == "\n":
                        var.lineo += 1
                    continue
                # // Comment line
                elif state == STATE.COMM_LINE:
                    if c == "\n":
                        var.lineo += 1
                        state = STATE.START
                    continue

                # < <=
                elif state == STATE.MINOR:
                    if c == '=':
                        currentToken.type = TokenType.LOREQ
                    else:
                        save = False
                        ungetChar = True if c else False
                        currentToken.type = TokenType.LT
                    state = STATE.DONE
                # > >=
                elif state == STATE.BIGGER:
                    if c == '=':
                        currentToken.type = TokenType.BOREQ
                    else:
                        save = False
                        ungetChar = True if c else False
                        currentToken.type = TokenType.BT
                    state = STATE.DONE

                # == != :=
                elif state == STATE.EQUAL:
                    if c == "=":
                        currentToken.type = TokenType.EQ
                    else:
                        save = False
                        ungetChar = True if c else False
                        currentToken.type = TokenType.ERROR
                    state = STATE.DONE
                elif state == STATE.NOT:
                    if c == "=":
                        currentToken.type = TokenType.DIFF
                    else:
                        save = False
                        ungetChar = True if c else False
                        currentToken.type = TokenType.ERROR
                    state = STATE.DONE
                elif state == STATE.ASSIGN:
                    if c == "=":
                        currentToken.type = TokenType.ASSIGN
                    else:
                        save = False
                        ungetChar = True if c else False
                        currentToken.type = TokenType.ERROR
                    state = STATE.DONE

            if save == True:
                currentToken.value += c
            var.posinfile = f.tell()
            if ungetChar: var.posinfile -= 1
        f.close()
        if(state == STATE.DONE and currentToken.type != TokenType.EOF):
            if(currentToken.type == TokenType.ID):
                currentToken.type = reservedLookUp(currentToken.value)
            #currentToken.value += '\0'
    if var.TraceScan:
        print(var.lineo + 1)
        print(currentToken.printToken(), end = '')
        var.output.write(str(var.lineo+1) + "\n" + currentToken.printToken())
    return currentToken
"""