import sys, os
sys.path.append(os.path.relpath("../enumTypes.py"))

from .tree import Tree
from enumTypes import TokenType

def syntaxError(msg, lineo):
    print(f'>>>Syntaxt error at line {lineo} {msg}' )

class Parser:
    def __init__(self, lex):
        self.lex = lex

    def parse(self):
        self.token = self.lex.getToken()
        tree = self.program()
        #tree.printPreOrder()
        if self.token.type != TokenType.EOF:
            syntaxError("Code ends before file", self.lex.lineo)
        return tree

    def match(self, expected):
        if self.token.type == expected:
            self.token = self.lex.getToken()
        else:
            syntaxError(f' expected {expected} received {self.token}', self.lex.lineo)

    # programa → main '{' lista-declaración lista-sentencias '}'
    def program(self):
        t = Tree("program")
        t.add_child(Tree("MAIN"))
        self.match(TokenType.MAIN)
        t.add_child(Tree("OPENC"))
        self.match(TokenType.OPENC)
        t.add_child(self.statementsList())
        t.add_child(self.sentencesList())

        t.add_child(Tree("CLOSEC"))
        self.match(TokenType.CLOSEC)
        return t

    # stmt-list→ { stmt; }
    def statementsList(self):
        t = Tree("STMT-LIST")
        options = [TokenType.INT, TokenType.REAL, TokenType.BOOLEAN]
        while self.token.type in options:
            t.add_child(self.statement())
        return t

    # stmt → type var-list
    def statement(self):
        t = Tree("STATEMENT")
        t.add_child(self.varType())
        t.add_child(self.varsList())
        return t

    # type → int | float | bool
    def varType(self):
        t = Tree("TYPE")
        if self.token.type == TokenType.INT:
            t.add_child(Tree("INT"))
            self.match(TokenType.INT)
        elif self.token.type == TokenType.REAL:
            t.add_child(Tree("REAL"))
            self.match(TokenType.REAL)
        elif self.token.type == TokenType.BOOLEAN:
            t.add_child(Tree("BOOLEAN"))
            self.match(TokenType.BOOLEAN)
        return t
    # vars-list → { identificador, } identificador
    def varsList(self):
        t = Tree("VAR-LIST")
        while self.token.type == TokenType.ID:
            id = Tree("ID")
            id.add_child(Tree(self.token.value))
            self.match(TokenType.ID)
            t.add_child(id)

            if self.token.type == TokenType.COMMA:
                self.match(TokenType.COMMA)
            else:
                break
        self.match(TokenType.SEMI);
        return t

    # sent-list → { sent }
    def sentencesList(self):
        t = Tree("SENT-LIST")
        options = [TokenType.IF, TokenType.WHILE, TokenType.CIN, TokenType.COUT, TokenType.OPENC, TokenType.ID]
        while self.token.type in options:
            t.add_child(self.sentence())
        return t

    # sent → select (if) | iteration (while) | sent-cin | sent-cout | block ( { ) | assign (id) 
    def sentence(self):
        t = Tree("SENTENCE")
        if self.token.type == TokenType.IF:
            t.add_child(self.select())
        elif self.token.type == TokenType.OPENC:
            t.add_child(self.block())
        elif self.token.type == TokenType.WHILE:
            t.add_child(self.iteration())
        elif self.token.type == TokenType.ID:
            t.add_child(self.assign())
        return t
    
    # iteration → while ( exp )  block
    def iteration(self):
        t = Tree("ITERATION")
        t.add_child(Tree("WHILE"))
        self.match(TokenType.WHILE)
        t.add_child(Tree("OPENP"))
        self.match(TokenType.OPENP)
        t.add_child(self.exp())
        t.add_child(Tree("CLOSEP"))
        self.match(TokenType.CLOSEP)
        t.add_child(self.block())
        return t

    # assign → id := exp ;  
    def assign(self):
        t = Tree("SENT-ASSIGN")
        id = Tree("ID")
        id.add_child(Tree(self.token.value))
        self.match(TokenType.ID)
        if self.token.type == TokenType.ASSIGN:
            id.add_child(Tree("ASSIGN"))
            self.match(TokenType.ASSIGN)
            id.add_child(self.exp())
        id.add_child(Tree("SEMI"))
        self.match(TokenType.SEMI)
        t.add_child(id)
        return t

    # sent-cin → cin id ;
    def sent_cin(self):
        t = Tree("SENT-CIN")
        t.add_child(Tree("CIN"))
        self.match(TokenType.CIN)
        id = Tree("ID")
        self.match(TokenType.ID)
        id.add_child(Tree(self.token.value))
        t.add_child(id)
        return t

    #  select → if ( exp ) then block [else block] end
    def select(self):
        t = Tree("SELECT")
        t.add_child(Tree("IF"))
        self.match(TokenType.IF)

        t.add_child(Tree("OPENP"))
        self.match(TokenType.OPENP)

        t.add_child(self.exp())

        t.add_child(Tree("CLOSEP"))
        self.match(TokenType.CLOSEP)

        t.add_child(Tree("THEN"))
        self.match(TokenType.THEN)
        t.add_child(self.block())
        if(self.token.type == TokenType.ELSE):
            t.add_child(Tree(self.token.value))
            self.match(TokenType.ELSE)
            t.add_child(self.block())
        t.add_child(Tree("END"))
        self.match(TokenType.END)
        return t

    # block → “{“ sent-list “ }”
    def block(self):
        t = Tree("BLOCK")
        t.add_child(Tree("OPENC"))
        self.match(TokenType.OPENC)
        t.add_child(self.sentencesList())
        t.add_child(Tree("CLOSEC"))
        self.match(TokenType.CLOSEC)
        return t

    #exp → exp-simple [relación exp-simple]
    def exp(self):
        t = Tree("EXP")
        t.add_child(self.simple_exp())
        options = [TokenType.LOREQ, TokenType.LT, TokenType.BT, TokenType.BOREQ, TokenType.EQ, TokenType.DIFF]
        if self.token.type in options:
            t.add_child(self.relation())
            t.add_child(self.simple_exp())
        return t

    #relacion → <= | < | > | >= | ==| !=
    def relation(self):
        t = Tree("RELATION")
        options = [TokenType.LOREQ, TokenType.LT, TokenType.BT, TokenType.BOREQ, TokenType.EQ, TokenType.DIFF]
        if self.token.type in options:
            t.add_child(Tree(self.token.value))
            self.match(self.token.type)
        else:
            syntaxError(f'unexpected token {self.token}', self.lex.lineo)
            self.token = self.lex.getToken()
        return t

    # exp-simple → term {suma-op term}
    def simple_exp(self):
        t = Tree("SIMPLE EXP")
        t.add_child(self.term())
        while(self.token.type in [TokenType.PLUS, TokenType.MINUS, TokenType.INC, TokenType.DEC]):
            t.add_child(self.add_op())
            t.add_child(self.term())
        return t

    # suma-op → + | - | ++ | --
    def add_op(self):
        t = Tree("ADD")
        options = [TokenType.PLUS, TokenType.MINUS]
        if self.token.type in options:
            t.add_child(Tree(self.token.value))
            self.match(self.token.type)
        elif self.token.type == TokenType.INC: #change this for a := a + 1
            t.add_child(Tree(self.token.value))
            self.match(TokenType.INC)
        elif self.token.type == TokenType.DEC: #change this for a := a - 1
            t.add_child(Tree(self.token.value))
            self.match(TokenType.DEC)
        else:
            syntaxError(f'unexpected token {self.token}', self.lex.lineo)
            self.token = self.lex.getToken()
        return t

    # term → factor {mult-op factor}
    def term(self):
        t = Tree("TERM")
        t.add_child(self.factor())
        while(self.token.type in [TokenType.MULT,TokenType.DIV,TokenType.MOD]):
            t.add_child(self.mult_op())
            t.add_child(self.factor())
        return t

    # mult-op → * | / |%
    def mult_op(self):
        t = Tree("MULT")
        options = [TokenType.MULT, TokenType.DIV, TokenType.MOD]
        if self.token.type in options:
            t.add_child(Tree(self.token.value))
            self.match(self.token.type)
        else:
            syntaxError(f'unexpected token {self.token}', self.lex.lineo)
            self.token = self.lex.getToken()
        return t

    # factor → ( exp ) | numero | id 
    def factor(self):
        t = Tree("FACTOR")
        if self.token.type == TokenType.OPENP:
            self.match(TokenType.OPENP)
            t.add_child(self.exp())
            self.match(TokenType.CLOSEP)
        elif self.token.type == TokenType.NUM:
            t.add_child(Tree(self.token.value))
            self.match(TokenType.NUM)
        elif self.token.type == TokenType.ID:
            t.add_child(Tree(self.token.value))
            self.match(TokenType.ID)
        else:
            syntaxError(f'unexpected token {self.token}', self.lex.lineo)
            self.token = self.lex.getToken()
        return t