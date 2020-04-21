from pathlib import Path 
#Local imports
from .token import Token
from .enumTypes import TokenType, STATE, reservedWords, uniqueCharacter, startSimbol

class Lexer:
    posinline = 0
    directory = ""
    output = ""
    file = ""
    lineo = 1
    traceScan = False

    def __init__(self, directory, file, traceScan = False, output = None):
        self.directory = directory
        self.file = directory + "/" + file
        self.traceScan = traceScan
        if traceScan:
            Path(directory+"/compilador").mkdir(parents=True, exist_ok=True)
            self.output = open(output,"w+") if output else open(directory+"/compilador/listing.txt","w+")

    def readfile(self):
        return (ln for ln in open(self.file, 'r'))
    
    def printCurrent(self, token, loc = True):
        location = str(self.lineo) + " " + str(self.posinline - len(token.value) + 1) if loc else ""
        print(location + "\n" + token.printToken(), end = '')
        self.output.write(location + "\n" + token.printToken())
    
    def checkStart(self, c):
        if c.isdigit():
            return STATE.NUM
        elif c.isalpha():
            return STATE.ID
        else:
            simbol = startSimbol.get(c)
            return simbol if simbol else STATE.UNIQUE

    def reservedLookUp(self, value):
        resWord = reservedWords.get(value)
        return resWord if resWord else TokenType.ID

    def uniqueLookUp(self, c):
        unique = uniqueCharacter.get(c)
        return unique if unique else TokenType.ERROR

    def run(self):
        tokens = []
        lines = self.readfile()
        for line in lines:
            self.posinline = 0
            currentToken = Token()
            while(self.posinline < len(line)):
                token = self.getToken(line, currentToken)
                if token.type == 0:
                    continue
                currentToken = Token()
                tokens.append(token)
            self.lineo += 1
        eofToken = Token(TokenType.EOF)
        tokens.append(eofToken)
        self.printCurrent(eofToken, False)
        return tokens
        if self.traceScan:
            self.output.close()

    def getToken(self, line, currentToken):
        state = STATE(0)
        while state != STATE.DONE:
            save = True
            ungetChar = False
            c = line[self.posinline]
            self.posinline += 1
            if state == STATE.START:
                if not c:
                    currentToken.type = TokenType.EOF
                    state = STATE.DONE
                    break
                state = self.checkStart(c)
                if state == STATE.SPACES:
                    state = STATE.START
                    if(c == '\n'):
                        state = STATE.DONE
                    continue
                # Unique character
                elif state == STATE.UNIQUE:
                    state = STATE.DONE
                    currentToken.type = self.uniqueLookUp(c)
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
                    elif c == '\n':
                        break
                    continue
                # */ Comment block end
                elif state == STATE.COMM_BLOCK_END:
                    if c == "/":
                        state = STATE.START
                    elif c != "*":
                        state = STATE.COMM_BLOCK
                    continue
                # // Comment line
                elif state == STATE.COMM_LINE:
                    if c == "\n":
                        break
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
            if ungetChar: self.posinline -= 1
        if(state == STATE.DONE and currentToken.type != TokenType.EOF):
            if(currentToken.type == TokenType.ID):
                currentToken.type = self.reservedLookUp(currentToken.value)
            #currentToken.value += '\0'
        if self.traceScan and currentToken.type != 0:
            self.printCurrent(currentToken)
        return currentToken


""" OLD METHOD, delete
def startLexicAnalysis():
    tokens = []
    while (True):
        token = getToken()
        tokens.append(token)
        if (token.type == TokenType.EOF):
            break
    #print(*tokens)"""