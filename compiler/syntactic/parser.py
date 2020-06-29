import sys, os
sys.path.append(os.path.relpath("../enumTypes"))
sys.path.append(os.path.relpath("../lexic"))

from pathlib import Path 
from .tree import Tree
from enumTypes import TokenType
from lexic.token import Token

#program follow { $ }
programFollow = [TokenType.EOF]

#stmt-list follow { if, while, cin, cout, “{”, id, “}” }
stmtListFollow = [
    TokenType.IF, TokenType.WHILE, TokenType.CIN,
    TokenType.COUT, TokenType.OPENC, TokenType.ID,
    TokenType.CLOSEC
]

#stmt follow { ; }
stmtFollow = [TokenType.SEMI]

#type follow { id }
typeFollow = [TokenType.ID]

#var-list follow { ; }
varListFollow = stmtFollow

#sent-list follow { “}” }
sentListFollow = [TokenType.CLOSEC]

#sent follow { if, while, cin, cout, “{”, id, “}” }
sentFollow = stmtListFollow

#select, iteration, cin, cout, block, assign follow { if, while, cin, cout, “{”, id, “}” }
selectFollow = stmtListFollow
iterationFollow = stmtListFollow
cinFollow = stmtListFollow
coutFollow = stmtListFollow
blockFollow = stmtListFollow
assignFollow = stmtListFollow

#common operators follow  { (, num, id }
operators = [TokenType.OPENP, TokenType.NUM, TokenType.ID]

#exp follow {  ),  ; }
expFollow = [TokenType.CLOSEP, TokenType.SEMI]

#relation follow  { (, num, id }
relationFollow = operators

#exp-simple follow  {  ),  ; }
simpleExpFollow = expFollow

#suma-op follow  { (, num, id }
addOpFollow = operators

#term follow { +, -, ++, - - , ),  ; }
termFollow = [
    TokenType.PLUS, TokenType.MINUS, 
    TokenType.INC, TokenType.DEC, 
    TokenType.CLOSEP, TokenType.SEMI
]

#mult-op follow  { (, num, id }
multOpFollow = operators

#factor follow { *, /, % , +, -, ++, - - , ),  ; }
factorFollow = [
    TokenType.MULT, TokenType.DIV, TokenType.MOD, 
    TokenType.PLUS, TokenType.MINUS, TokenType.INC, 
    TokenType.DEC, TokenType.CLOSEP, TokenType.SEMI
]

def inc_dec(last, t, inc):
    assign = Token(TokenType.ASSIGN, ":=", last.lineo)
    inc_dec = Token(TokenType.PLUS, "+", last.lineo) if inc == True else Token(TokenType.MINUS, "-", last.lineo)
    one = Token(TokenType.NUM, "1", last.lineo)
    t.add_child(Tree(assign))
    t.add_child(Tree(last))
    t.add_child(Tree(inc_dec))
    t.add_child(Tree(one))

class Error:
    def __init__(self, message = "", lineo = 0):
        self.message = message
        self.lineo = lineo

class Parser:
    def __init__(self, lex, directory, traceParser = False):
        self.lex = lex
        self.directory = directory
        self.traceParser = traceParser
        Path(directory+"/compilador").mkdir(parents=True, exist_ok=True)
        self.output = open(directory+"/compilador/syntactic.o","w+")
        self.error = Error()

    def parse(self):
        self.token = self.lex.getToken()
        tree = self.program(programFollow)
        tree.build(self.directory)
        if self.traceParser:
            tree.printPreOrder()
        if self.token.type != TokenType.EOF:
            self.syntaxError("Code ends before file", self.lex.lineo)
        return tree

    def getToken(self):
        if self.token.type != TokenType.EOF:
            self.token = self.lex.getToken()

    def syntaxError(self, msg, lineo):
        out = f'>>>Syntaxt error at line {lineo} {msg}'
        self.output.write(out + "\n")
        if self.traceParser:
            print(out)
        

    def match(self, expected, parent=None, child=None):
        self.last = self.token
        if self.token.type == expected:
            self.getToken()
            if parent is not None:
                if child is None:
                    parent.add_child(Tree(self.last))
                else:
                    parent.add_child(child)
        else:
            self.syntaxError(f' expected {expected} received {self.token}', self.lex.lineo)
            self.getToken()

    # programa → main '{' lista-declaración lista-sentencias '}'
    def program(self, follow):
        t = Tree("program")
        #first main
        first = [TokenType.MAIN]
        self.checkInput(first, follow)
        if self.token.type in first:
            self.match(TokenType.MAIN, t)
            self.checkInput([TokenType.OPENC], follow)
            self.match(TokenType.OPENC)
            t.add_child(self.statementsList(stmtListFollow))
            t.add_child(self.sentencesList(sentListFollow))
            self.checkInput([TokenType.CLOSEC], follow)
            self.match(TokenType.CLOSEC)
            self.checkInput(follow, first)
        return t

    # stmt-list→ { stmt; }
    def statementsList(self, follow):
        t = Tree("STMT-LIST")
        #first { int, float, bool , e}
        first = [TokenType.INT, TokenType.REAL, TokenType.BOOLEAN]
        #self.checkInput(first, follow)
        if self.token.type in first:
            while self.token.type in first:
                t.add_child(self.statement(stmtFollow))
                self.match(TokenType.SEMI)
            #self.checkInput(follow, first)
        return t

    # stmt → type var-list
    def statement(self, follow):
        t = Tree("STATEMENT")
        first = [TokenType.INT, TokenType.REAL, TokenType.BOOLEAN]
        self.checkInput(first, follow)
        if self.token.type in first:
            t.add_child(self.varType(typeFollow))
            t.add_child(self.varsList(varListFollow))
            self.checkInput(follow, first)
        return t

    # type → int | float | bool
    def varType(self, follow):
        t = Tree("TYPE")
        first = [TokenType.INT, TokenType.REAL, TokenType.BOOLEAN]
        self.checkInput(first, follow)
        if self.token.type in first:
            if self.token.type == TokenType.INT:
                self.match(TokenType.INT, t)
            elif self.token.type == TokenType.REAL:
                self.match(TokenType.REAL, t)
            elif self.token.type == TokenType.BOOLEAN:
                self.match(TokenType.BOOLEAN, t)
            else:
                self.syntaxError(f'unexpected token {self.token}', self.lex.lineo)
            self.checkInput(follow, first)
        return t

    # vars-list → { identificador, } identificador
    def varsList(self, follow):
        t = Tree("VAR-LIST")
        first = [TokenType.ID]
        self.checkInput(first, follow)
        if self.token.type in first:
            self.match(TokenType.ID, t)
            while self.token.type == TokenType.COMMA:
                self.match(TokenType.COMMA)
                self.match(TokenType.ID, t)
            self.checkInput(follow, first)
        return t

    # sent-list → { sent }
    def sentencesList(self, follow):
        t = Tree("SENT-LIST")
        #first {if, while, cin, cout, “{”, id, e}
        first = [TokenType.IF, TokenType.WHILE, TokenType.CIN, TokenType.COUT, TokenType.OPENC, TokenType.ID]
        #self.checkInput(first, follow)
        if self.token.type in first:
            while self.token.type in first:
                t.add_child(self.sentence(sentFollow))
            #self.checkInput(follow, first)
        return t

    # sent → select (if) | iteration (while) | sent-cin | sent-cout | block ( { ) | assign (id) 
    def sentence(self, follow):
        t = Tree("SENTENCE")
        #first {if, while, cin, cout, “{”, id}
        first = [TokenType.IF, TokenType.WHILE, TokenType.CIN, TokenType.COUT, TokenType.OPENC, TokenType.ID]
        self.checkInput(first, follow)
        if self.token.type in first:
            if self.token.type == TokenType.IF:
                t.add_child(self.select(selectFollow))
            elif self.token.type == TokenType.CIN:
                t.add_child(self.sent_cin(cinFollow))
            elif self.token.type == TokenType.COUT:
                t.add_child(self.sent_cout(coutFollow))
            elif self.token.type == TokenType.OPENC:
                t.add_child(self.block(blockFollow))
            elif self.token.type == TokenType.WHILE:
                t.add_child(self.iteration(iterationFollow))
            elif self.token.type == TokenType.ID:
                t.add_child(self.assign(assignFollow))
            self.checkInput(follow, first)
        return t
    
    # iteration → while ( exp )  block
    def iteration(self, follow):
        t = Tree("ITERATION")
        first = [TokenType.WHILE]
        self.checkInput(first, follow)
        if self.token.type in first:
            self.match(TokenType.WHILE, t)
            self.match(TokenType.OPENP)
            t.add_child(self.exp(expFollow))
            self.match(TokenType.CLOSEP)
            t.add_child(self.block(blockFollow))
            self.checkInput(follow, first)
        return t

    # assign → id := exp ;  
    def assign(self, follow):
        t = Tree("SENT-ASSIGN")
        first = [TokenType.ID]
        self.checkInput(first, follow)
        if self.token.type in first:
            self.match(TokenType.ID, t)
            if self.token.type == TokenType.ASSIGN:
                self.match(TokenType.ASSIGN, t)
                t.add_child(self.exp(expFollow))
            elif self.token.type == TokenType.INC:
                inc_dec(self.last, t, True)
                self.match(TokenType.INC)
            elif self.token.type == TokenType.DEC:
                inc_dec(self.last, t, False)
                self.match(TokenType.DEC)
            else:
                self.syntaxError(f'unexpected token {self.token}', self.lex.lineo)
            self.match(TokenType.SEMI)
            self.checkInput(follow, first)
        return t

    # sent-cin → cin id ;
    def sent_cin(self, follow):
        t = Tree("SENT-CIN")
        first = [TokenType.CIN]
        self.checkInput(first, follow)
        if self.token.type in first:
            self.match(TokenType.CIN, t)
            self.match(TokenType.ID, t)
            # FIXME:
            self.match(TokenType.SEMI)
            self.checkInput(follow, first)
        return t
    
    # sent-cout → cout exp ;
    def sent_cout(self, follow):
        t = Tree("SENT-COUT")
        first = [TokenType.COUT]
        self.checkInput(first, follow)
        if self.token.type in first:
            self.match(TokenType.COUT, t)
            # FIXME:
            exp = self.exp(expFollow)
            self.match(TokenType.SEMI, t, exp)
            self.checkInput(follow, first)
        return t

    #  select → if ( exp ) then block [else block] end
    def select(self, follow):
        t = Tree("SELECT")
        #first  { if }
        first = [TokenType.IF]
        self.checkInput(first, follow)
        if self.token.type in first:
            self.match(TokenType.IF, t)
            self.match(TokenType.OPENP)
            t.add_child(self.exp(expFollow))
            self.match(TokenType.CLOSEP)
            self.match(TokenType.THEN, t)
            t.add_child(self.block(blockFollow))
            if(self.token.type == TokenType.ELSE):
                self.match(TokenType.ELSE, t)
                t.add_child(self.block(blockFollow))
            self.match(TokenType.END, t)
            self.checkInput(follow, first)
        return t

    # block → “{“ sent-list “ }”
    def block(self, follow):
        t = Tree("BLOCK")
        first = [TokenType.OPENC]
        self.checkInput(first, follow)
        if self.token.type in first:
            self.match(TokenType.OPENC)
            t.add_child(self.sentencesList(sentListFollow))
            self.match(TokenType.CLOSEC)
            self.checkInput(follow, first)
        return t

    #exp → exp-simple [relación exp-simple]
    def exp(self, follow):
        t = Tree("EXP")
        # first { (, num, id }
        first = [TokenType.OPENP, TokenType.NUM, TokenType.ID]
        self.checkInput(first, follow)
        if self.token.type in first:
            t.add_child(self.simple_exp(simpleExpFollow))
            options = [TokenType.LOREQ, TokenType.LT, TokenType.BT, TokenType.BOREQ, TokenType.EQ, TokenType.DIFF]
            if self.token.type in options:
                t.add_child(self.relation(relationFollow))
                t.add_child(self.simple_exp(simpleExpFollow))
            self.checkInput(follow, first)
        return t

    #relacion → <= | < | > | >= | ==| !=
    def relation(self, follow):
        t = Tree("RELATION")
        #first { <= , < , > , >= , = , != }
        first = [TokenType.LOREQ, TokenType.LT, TokenType.BT, TokenType.BOREQ, TokenType.EQ, TokenType.DIFF]
        self.checkInput(first, follow)
        if self.token.type in first:
            if self.token.type in first:
                self.match(self.token.type, t)
            else:
                self.syntaxError(f'unexpected token {self.token}', self.lex.lineo)
            self.checkInput(follow, first)
        return t

    # exp-simple → term {suma-op term}
    def simple_exp(self, follow):
        t = Tree("SIMPLE EXP")
        # first { (, num, id }
        first = [TokenType.OPENP, TokenType.NUM, TokenType.ID]
        self.checkInput(first, follow)
        if self.token.type in first:
            t.add_child(self.term(termFollow))
            while(self.token.type in [TokenType.PLUS, TokenType.MINUS, TokenType.INC, TokenType.DEC]):
                type = self.token.type
                t.add_child(self.add_op(addOpFollow))
                if type is not TokenType.INC and type is not TokenType.DEC:
                    t.add_child(self.term(termFollow))
            self.checkInput(follow, first)
        return t

    # suma-op → + | - | ++ | --
    def add_op(self, follow):
        t = Tree("ADD")
        #first { +, -, ++, - - }
        first = [TokenType.PLUS, TokenType.MINUS, TokenType.INC, TokenType.DEC]
        self.checkInput(first, follow)
        if self.token.type in first:
            options = [TokenType.PLUS, TokenType.MINUS]
            if self.token.type in options:
                self.match(self.token.type, t)
            elif self.token.type == TokenType.INC: #change this for a := a + 1
                inc_dec(self.last, t, True)
                self.match(TokenType.INC)
            elif self.token.type == TokenType.DEC: #change this for a := a - 1
                inc_dec(self.last, t, False)
                self.match(TokenType.DEC)
            self.checkInput(follow, first)
        return t

    # term → factor {mult-op factor}
    def term(self, follow):
        t = Tree("TERM")
        #first { (, num, id }
        first = [TokenType.OPENP, TokenType.NUM, TokenType.ID]
        self.checkInput(first, follow)
        if self.token.type in first:
            t.add_child(self.factor(factorFollow))
            while(self.token.type in [TokenType.MULT,TokenType.DIV,TokenType.MOD]):
                t.add_child(self.mult_op(multOpFollow))
                t.add_child(self.factor(factorFollow))
            self.checkInput(follow, first)
        return t

    # mult-op → * | / |%
    def mult_op(self, follow):
        t = Tree("MULT")
        # first { *, /, % }
        first = [TokenType.MULT, TokenType.DIV, TokenType.MOD]
        self.checkInput(first, follow)
        if self.token.type in first:
            if self.token.type in first:
                self.match(self.token.type, t)
            else:
                self.syntaxError(f'unexpected token {self.token}', self.lex.lineo)
            self.checkInput(follow, first)
        return t

    # factor → ( exp ) | numero | id 
    def factor(self, follow):
        t = Tree("FACTOR")
        # first { (, num, id }
        first = [TokenType.OPENP, TokenType.NUM, TokenType.ID]
        self.checkInput(first, follow)
        if self.token.type in first:
            if self.token.type == TokenType.OPENP:
                self.match(TokenType.OPENP)
                t.add_child(self.exp(expFollow))
                self.match(TokenType.CLOSEP)
            elif self.token.type == TokenType.NUM:
                self.match(TokenType.NUM, t)
            elif self.token.type == TokenType.ID:
                self.match(TokenType.ID, t)
            else:
                self.syntaxError(f'unexpected token {self.token}', self.lex.lineo)
            self.checkInput(follow, first)
        return t

    def checkInput(self, first, follow):
        if self.token.type not in first:
            newError = Error(f'unexpected token {self.token}', self.lex.lineo)
            if self.error.message != newError.message and self.error.lineo != newError.lineo:
                self.error = newError
                self.syntaxError(self.error.message, self.lex.lineo)
            self.scanTo(first + follow)

    def scanTo(self, follow):
        while self.token.type not in follow + [TokenType.EOF]:
            self.token = self.lex.getToken()