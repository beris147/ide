import sys, os
sys.path.append(os.path.relpath("../enumTypes.py"))

from pathlib import Path 
#Local imports
from .token import Token
from enumTypes import TokenType, STATE, reservedWords, uniqueCharacter, startSimbol

class Lex:
    def __init__(self, directory, file, traceScan = False, output = None):
        self.directory = directory
        self.file = directory + "/" + file
        self.traceScan = traceScan
        self.posinline = 0
        self.lineo = 1
        self.state = STATE(0)
        self.readed = False
        self.lines = list()
        if traceScan:
            Path(directory+"/compilador").mkdir(parents=True, exist_ok=True)
            self.output = open(output,"w+") if output else open(directory+"/compilador/listing.txt","w+")

    def readfile(self):
        return (ln + '\n' for ln in open(self.file, 'r'))
    
    def printCurrent(self, token, loc = True):
        location = str(self.lineo) + " " + str(self.posinline - len(token.value) + 1) if loc else ""
        print(location + "\n" + token.printToken(), end = '')
        if self.traceScan:
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
    
    def getNextChar(self):
        #File not readed yet
        if self.readed == False:
            self.lines = list(self.readfile())
            self.readed = True
        #end of line
        if self.posinline >= len(self.lines[self.lineo-1]):
            self.lineo += 1
            self.posinline = 0
        #end of file
        if self.lineo-1 >= len(self.lines):
            return None
        #next char
        c = self.lines[self.lineo-1][self.posinline]
        self.posinline += 1
        return c

    def getToken(self):
        currentToken = Token()
        self.state = STATE(0)
        while self.state != STATE.DONE:
            save = True
            ungetChar = False
            c = self.getNextChar()
            #c = line[self.posinline]
            #self.posinline += 1
            if(len(currentToken.value)+1 > 31):
                currentToken.type = TokenType.ERROR
                self.state = STATE.DONE
                save = False
                ungetChar = True
            if self.state == STATE.START:
                if not c:
                    currentToken.type = TokenType.EOF
                    self.state = STATE.DONE
                    break
                self.state = self.checkStart(c)
                if self.state == STATE.SPACES:
                    self.state = STATE.START
                    #if(c == '\n'):
                    #    self.state = STATE.DONE
                    continue
                # Unique character
                elif self.state == STATE.UNIQUE:
                    self.state = STATE.DONE
                    currentToken.type = self.uniqueLookUp(c)
            # Identifiers
            else:
                if self.state == STATE.ID:
                    if not (c.isalnum() or c == "_"):
                        save = False
                        ungetChar = True if c else False
                        currentToken.type = TokenType.ID
                        self.state = STATE.DONE

                # Numbers
                elif self.state == STATE.NUM:
                    if c == ".":
                        self.state = STATE.DOT
                    elif not c.isdigit():
                        save = False
                        ungetChar = True if c else False
                        currentToken.type = TokenType.NUM if currentToken.value[0].isdigit() else TokenType.SNUM
                        self.state = STATE.DONE                
                # Dot .
                elif self.state == STATE.DOT:
                    if c.isdigit():
                        self.state = STATE.FLOAT
                    else:
                        save = False
                        ungetChar = True if c else False
                        currentToken.type = TokenType.ERROR
                        self.state = STATE.DONE
                # Float numbers
                elif self.state == STATE.FLOAT:
                    if not c.isdigit():
                        save = False
                        ungetChar = True if c else False
                        currentToken.type = TokenType.FLOAT if currentToken.value[0].isdigit() else TokenType.SFLOAT
                        self.state = STATE.DONE

                # +
                elif self.state == STATE.PLUS:
                    # if c.isdigit():
                    #     self.state = STATE.NUM
                    if c == "+":
                        currentToken.type = TokenType.INC
                        self.state = STATE.DONE
                    else:
                        save = False
                        ungetChar = True if c else False
                        currentToken.type = TokenType.PLUS
                        self.state = STATE.DONE

                # -
                elif self.state == STATE.MINUS:
                    # if c.isdigit():
                    #     self.state = STATE.NUM
                    if c == "-":
                        currentToken.type = TokenType.DEC
                        self.state = STATE.DONE
                    else:
                        save = False
                        ungetChar = True if c else False
                        currentToken.type = TokenType.MINUS
                        self.state = STATE.DONE

                # /
                elif self.state == STATE.DIAG:
                    if c == "*":
                        self.state = STATE.COMM_BLOCK
                        currentToken.value = ""
                        continue
                    elif c == "/":
                        self.state = STATE.COMM_LINE
                        currentToken.value = ""
                        continue
                    else:
                        save = False
                        ungetChar = True if c else False
                        currentToken.type = TokenType.DIV
                        self.state = STATE.DONE

                # /* Comment block
                elif self.state == STATE.COMM_BLOCK:
                    if c == "*":
                        self.state = STATE.COMM_BLOCK_END
                    #elif c == '\n':
                    #    break
                    continue
                # */ Comment block end
                elif self.state == STATE.COMM_BLOCK_END:
                    if c == "/":
                        self.state = STATE.START
                    elif c == '\n':
                        self.state = STATE.COMM_BLOCK
                        break
                    elif c != "*":
                        self.state = STATE.COMM_BLOCK
                    continue
                # // Comment line
                elif self.state == STATE.COMM_LINE:
                    if c == "\n":
                        self.state = STATE.START
                        break
                    continue

                # < <=
                elif self.state == STATE.MINOR:
                    if c == '=':
                        currentToken.type = TokenType.LOREQ
                    else:
                        save = False
                        ungetChar = True if c else False
                        currentToken.type = TokenType.LT
                    self.state = STATE.DONE
                # > >=
                elif self.state == STATE.BIGGER:
                    if c == '=':
                        currentToken.type = TokenType.BOREQ
                    else:
                        save = False
                        ungetChar = True if c else False
                        currentToken.type = TokenType.BT
                    self.state = STATE.DONE

                # == != :=
                elif self.state == STATE.EQUAL:
                    if c == "=":
                        currentToken.type = TokenType.EQ
                    else:
                        save = False
                        ungetChar = True if c else False
                        currentToken.type = TokenType.ERROR
                    self.state = STATE.DONE
                elif self.state == STATE.NOT:
                    if c == "=":
                        currentToken.type = TokenType.DIFF
                    else:
                        save = False
                        ungetChar = True if c else False
                        currentToken.type = TokenType.ERROR
                    self.state = STATE.DONE
                elif self.state == STATE.ASSIGN:
                    if c == "=":
                        currentToken.type = TokenType.ASSIGN
                    else:
                        save = False
                        ungetChar = True if c else False
                        currentToken.type = TokenType.ERROR
                    self.state = STATE.DONE
            if save == True:
                currentToken.value += c
            if ungetChar: self.posinline -= 1
        if(self.state == STATE.DONE and currentToken.type != TokenType.EOF):
            if(currentToken.type == TokenType.ID):
                currentToken.type = self.reservedLookUp(currentToken.value)
        if self.traceScan and currentToken.type != 0:
            self.printCurrent(currentToken)
        return currentToken