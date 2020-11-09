import sys, os
sys.path.append(os.path.relpath("../enumTypes"))
sys.path.append(os.path.relpath("../lexic"))

from pathlib import Path 
from .tree import ATS
from enumTypes import TokenType
from lexic.token import Token

#program follow { $ }
programFollow = [TokenType.EOF]

#stmt-list follow { if, while, cin, cout, “{”, id, “}” }
stmtListFollow = [
    TokenType.IF, TokenType.WHILE, TokenType.UNTIL, TokenType.CIN,
    TokenType.COUT, TokenType.OPENC, TokenType.ID,
    TokenType.CLOSEC, TokenType.DO, TokenType.INT,
    TokenType.REAL, TokenType.BOOLEAN, TokenType.END, TokenType.ELSE
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
blockFollow = stmtListFollow + [TokenType.ELSE, TokenType.END]
assignFollow = stmtListFollow
repeatFollow = stmtListFollow

#common operators follow  { (, num, id }
operators = [TokenType.OPENP, TokenType.NUM, TokenType.REAL, TokenType.ID]

#exp follow {  ),  ; }
expFollow = [TokenType.CLOSEP, TokenType.SEMI]

#relation follow  { (, num, id }
relationFollow = operators

relationOperators = [TokenType.LOREQ, TokenType.LT, TokenType.BT, TokenType.BOREQ, TokenType.EQ, TokenType.DIFF]

#exp-simple follow  {  ),  ;, <= , < , > , >= , = , != }
simpleExpFollow = expFollow + relationOperators

#suma-op follow  { (, num, id }
addOpFollow = operators

#term follow { +, -, ++, - - , ),  ;, <= , < , > , >= , = , != }
termFollow = [
    TokenType.PLUS, TokenType.MINUS, 
    TokenType.INC, TokenType.DEC, 
    TokenType.CLOSEP, TokenType.SEMI
] + relationOperators

#mult-op follow  { (, num, id }
multOpFollow = operators

#factor follow { *, /, % , +, -, ++, - - , ),  ;, <= , < , > , >= , = , != }
factorFollow = [
    TokenType.MULT, TokenType.DIV, TokenType.MOD, 
    TokenType.PLUS, TokenType.MINUS, TokenType.INC, 
    TokenType.DEC, TokenType.CLOSEP, TokenType.SEMI
] + relationOperators


def get_mock_term(value):
    term = ATS("TERM")
    fact = ATS("FACTOR")
    fact.add_child(ATS(value))
    term.add_child(fact)
    return term

def get_mock_exp(node, a, b):
    simple = ATS("SIMPLE-EXP")
    node.add_child(get_mock_term(a))
    node.add_child(get_mock_term(b))
    simple.add_child(node)
    exp = ATS("EXP")
    exp.add_child(simple)
    return exp

def inc_dec(last, inc):
    assign = ATS(Token(TokenType.ASSIGN, ":=", last.lineo))
    inc_dec = ATS(Token(TokenType.PLUS, "+", last.lineo)) if inc == True else ATS(Token(TokenType.MINUS, "-", last.lineo))
    one = Token(TokenType.NUM, "1", last.lineo)
    assign.add_child(ATS(last))
    assign.add_child(get_mock_exp(inc_dec, last, one))
    return assign

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
        self.lastError = 0

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
        if self.lastError != lineo:
            self.lastError = lineo
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
                    parent.add_child(ATS(self.last))
                else:
                    parent.add_child(child)
        else:
            self.syntaxError(f' expected {expected} received {self.token}', self.lex.lineo)

    # programa → main '{' lista-declaración lista-sentencias '}' $ 
    def program(self, follow):
        t = ATS("program")
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
        t = ATS("STMT-LIST")
        #first { int, float, bool , e}
        first = [TokenType.INT, TokenType.REAL, TokenType.BOOLEAN]
        self.checkInput(first, follow)
        if self.token.type in first:
            while self.token.type in first:
                t.add_child(self.statement(stmtFollow))
                self.match(TokenType.SEMI)
                self.checkInput(follow, first)
        return t

    # stmt → type var-list
    def statement(self, follow):
        t = ATS("STMT")
        first = [TokenType.INT, TokenType.REAL, TokenType.BOOLEAN]
        self.checkInput(first, follow)
        if self.token.type in first:
            stmt = self.varType(typeFollow)
            stmt.add_child(self.varsList(varListFollow))
            t.add_child(stmt)
        return t

    # type → int | float | bool
    def varType(self, follow):
        t = ATS("TYPE")
        first = [TokenType.INT, TokenType.REAL, TokenType.BOOLEAN]
        self.checkInput(first, follow)
        if self.token.type in first:
            t = ATS(self.token)
            if self.token.type == TokenType.INT:
                self.match(TokenType.INT)
            elif self.token.type == TokenType.REAL:
                self.match(TokenType.REAL)
            elif self.token.type == TokenType.BOOLEAN:
                self.match(TokenType.BOOLEAN)
            else:
                self.syntaxError(f'unexpected token {self.token}', self.lex.lineo)
            self.checkInput(follow, first)
        return t

    # vars-list → { identificador, } identificador
    def varsList(self, follow):
        t = ATS("VAR-LIST")
        first = [TokenType.ID]
        self.checkInput(first, follow)
        if self.token.type in first:
            self.match(TokenType.ID, t)
            while self.token.type == TokenType.COMMA:
                self.match(TokenType.COMMA)
                self.match(TokenType.ID, t)
            #self.checkInput(follow, first)
        return t

    # sent-list → { sent }
    def sentencesList(self, follow):
        t = ATS("SENT-LIST")
        #first {if, while, cin, cout, “{”, id, e}
        first = [TokenType.IF, TokenType.WHILE, TokenType.CIN, TokenType.COUT, TokenType.OPENC, TokenType.ID, TokenType.DO]
        self.checkInput(first, follow)
        if self.token.type in first:
            while self.token.type in first:
                t.add_child(self.sentence(sentFollow))
            #self.checkInput(follow, first)
        return t

    # sent → select (if) | iteration (while) | sent-cin | sent-cout | block ( { ) | assign (id) 
    def sentence(self, follow):
        t = ATS("SENT")
        #first {if, while, cin, cout, “{”, id}
        first = [
            TokenType.IF, TokenType.WHILE, 
            TokenType.CIN, TokenType.COUT, 
            TokenType.OPENC, TokenType.ID, 
            TokenType.DO
        ]
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
            elif self.token.type == TokenType.DO:
                t.add_child(self.repeat(repeatFollow))
            self.checkInput(follow, first)
        return t
    
    # repeat → do block until ( exp );
    def repeat(self, follow):
        t = ATS("REPEAT")
        first = [TokenType.DO]
        self.checkInput(first, follow)
        if self.token.type in first:
            self.match(TokenType.DO, t)
            if self.token.type == TokenType.OPENC:
                t.add_child(self.block(blockFollow))
            else:
                t.add_child(self.sentencesList(sentListFollow))
            self.match(TokenType.UNTIL, t)
            self.match(TokenType.OPENP)
            t.add_child(self.exp(expFollow))
            self.match(TokenType.CLOSEP)
            self.match(TokenType.SEMI)
            self.checkInput(follow, first)
        return t

    # iteration → while ( exp )  block
    def iteration(self, follow):
        t = ATS("ITERATION")
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
        t = ATS("SENT-ASSIGN")
        first = [TokenType.ID]
        self.checkInput(first, follow)
        if self.token.type in first:
            id = ATS(self.token)
            self.match(TokenType.ID)
            if self.token.type == TokenType.ASSIGN:
                parent = ATS(self.token)
                self.match(TokenType.ASSIGN)
                parent.add_child(id)
                parent.add_child(self.exp(expFollow))
                t.add_child(parent)
            elif self.token.type == TokenType.INC:
                t.add_child(inc_dec(self.last, True))
                self.match(TokenType.INC)
            elif self.token.type == TokenType.DEC:
                t.add_child(inc_dec(self.last, False))
                self.match(TokenType.DEC)
            else:
                self.syntaxError(f'unexpected token {self.token}', self.lex.lineo)
            self.match(TokenType.SEMI)
            self.checkInput(follow, first)
        return t

    # sent-cin → cin id ;
    def sent_cin(self, follow):
        t = ATS("SENT-CIN")
        first = [TokenType.CIN]
        self.checkInput(first, follow)
        if self.token.type in first:
            cin = ATS(self.token)
            self.match(TokenType.CIN)
            self.match(TokenType.ID, cin)
            t.add_child(cin)
            self.match(TokenType.SEMI)
            self.checkInput(follow, first)
        return t
    
    # sent-cout → cout exp ;
    def sent_cout(self, follow):
        t = ATS("SENT-COUT")
        first = [TokenType.COUT]
        self.checkInput(first, follow)
        if self.token.type in first:
            cout = ATS(self.token)
            self.match(TokenType.COUT)
            exp = self.exp(expFollow)
            cout.add_child(exp)
            t.add_child(cout)
            self.match(TokenType.SEMI)
            self.checkInput(follow, first)
        return t

    #  select → if ( exp ) then block [else block] end
    def select(self, follow):
        t = ATS("SELECT")
        first = [TokenType.IF]
        self.checkInput(first, follow)
        if self.token.type in first:
            self.match(TokenType.IF, t)
            self.match(TokenType.OPENP)
            t.add_child(self.exp(expFollow))
            self.match(TokenType.CLOSEP)
            self.match(TokenType.THEN, t)
            if self.token.type == TokenType.OPENC:
                t.add_child(self.block(blockFollow))
            else:
                t.add_child(self.sentencesList(sentListFollow))
            if(self.token.type == TokenType.ELSE):
                self.match(TokenType.ELSE, t)
                if self.token.type == TokenType.OPENC:
                    t.add_child(self.block(blockFollow))
                else:
                    t.add_child(self.sentencesList(sentListFollow))
            self.match(TokenType.END, t)
            self.checkInput(follow, first)
        return t

    # block → “{“ sent-list “ }”
    def block(self, follow):
        t = ATS("BLOCK")
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
        t = ATS("EXP")
        # first { (, num, id }
        first = [TokenType.OPENP, TokenType.NUM, TokenType.REAL, TokenType.ID]
        self.checkInput(first, follow)
        if self.token.type in first:
            parent = self.simple_exp(simpleExpFollow)
            options = [TokenType.LOREQ, TokenType.LT, TokenType.BT, TokenType.BOREQ, TokenType.EQ, TokenType.DIFF]
            if self.token.type in options:
                aux = parent
                parent = ATS("RELATION")
                child = self.relation(relationFollow)
                child.add_child(aux)
                child.add_child(self.simple_exp(simpleExpFollow))
                parent.add_child(child)
            t.add_child(parent)
            self.checkInput(follow, first)
        return t

    #relacion → <= | < | > | >= | ==| !=
    def relation(self, follow):
        t = ATS("RELATION")
        #first { <= , < , > , >= , = , != }
        first = [TokenType.LOREQ, TokenType.LT, TokenType.BT, TokenType.BOREQ, TokenType.EQ, TokenType.DIFF]
        self.checkInput(first, follow)
        if self.token.type in first:
            if self.token.type in first:
                t = ATS(self.token)
                self.match(self.token.type)
            else:
                self.syntaxError(f'unexpected token {self.token}', self.lex.lineo)
            self.checkInput(follow, first)
        return t

    # exp-simple → term {suma-op term}
    def simple_exp(self, follow):
        t = ATS("SIMPLE-EXP")
        # first { (, num, id }
        first = [TokenType.OPENP, TokenType.NUM,  TokenType.REAL, TokenType.ID]
        self.checkInput(first, follow)
        if self.token.type in first:
            parent = self.term(termFollow)
            while(self.token.type in [TokenType.PLUS, TokenType.MINUS, TokenType.INC, TokenType.DEC]):
                type = self.token.type
                if type is not TokenType.INC and type is not TokenType.DEC:
                    aux = parent
                    parent = self.add_op(addOpFollow)
                    parent.add_child(aux)
                    parent.add_child(self.term(termFollow))
                else:
                    t = inc_dec(self.last, self.last.type == TokenType.INC)
                    self.match(self.token.type)
            t.add_child(parent)
            self.checkInput(follow, first)
        return t

    # suma-op → + | - | ++ | --
    def add_op(self, follow):
        t = ATS()
        #first { +, -, ++, - - }
        first = [TokenType.PLUS, TokenType.MINUS, TokenType.INC, TokenType.DEC]
        self.checkInput(first, follow)
        if self.token.type in first:
            options = [TokenType.PLUS, TokenType.MINUS]
            if self.token.type in options:
                t = ATS(self.token)
                self.match(self.token.type)
            elif self.token.type == TokenType.INC: #change this for a := a + 1 FALTA
                t = inc_dec(self.last, True)
                self.match(TokenType.INC)
            elif self.token.type == TokenType.DEC: #change this for a := a - 1
                t = inc_dec(self.last, False)
                self.match(TokenType.DEC)
            self.checkInput(follow, first)
        return t

    # term → factor {mult-op factor}
    def term(self, follow):
        t = ATS("TERM")
        #first { (, num, id }
        first = [TokenType.OPENP, TokenType.NUM,  TokenType.REAL, TokenType.ID]
        self.checkInput(first, follow)
        if self.token.type in first:
            parent = self.factor(factorFollow)
            while(self.token.type in [TokenType.MULT,TokenType.DIV,TokenType.MOD]):
                aux = parent
                parent = self.mult_op(multOpFollow)
                parent.add_child(aux)
                parent.add_child(self.factor(factorFollow))
            t.add_child(parent)
            self.checkInput(follow, first)
        return t

    # mult-op → * | / |%
    def mult_op(self, follow):
        t = ATS("MULT-OP")
        # first { *, /, % }
        first = [TokenType.MULT, TokenType.DIV, TokenType.MOD]
        self.checkInput(first, follow)
        if self.token.type in first:
            if self.token.type in first:
                t = ATS(self.token)
                self.match(self.token.type)
            else:
                self.syntaxError(f'unexpected token {self.token}', self.lex.lineo)
            self.checkInput(follow, first)
        return t

    # factor → ( exp ) | numero | id 
    def factor(self, follow):
        t = ATS("FACTOR")
        # first { (, num, id }
        first = [TokenType.OPENP, TokenType.NUM,  TokenType.REAL, TokenType.ID]
        self.checkInput(first, follow)
        if self.token.type in first:
            if self.token.type == TokenType.OPENP:
                self.match(TokenType.OPENP)
                t.add_child(self.exp(expFollow))
                self.match(TokenType.CLOSEP)
            elif self.token.type == TokenType.NUM or self.token.type == TokenType.REAL:
                self.match(self.token.type, t)
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