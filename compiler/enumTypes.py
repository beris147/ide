import enum
class TokenType(enum.Enum): 
    #IDENTIFICADOR
    ID = 1
    #NUMEROS ENTEROS CON Y SIN SIGNO
    NUM = 2
    SNUM = 3
    #NUMEROS FLOTANTES CON Y SIN SIGNO
    FLOAT = 4
    SFLOAT = 5
    #SÍMBOLOS LÓGICOS
    LT = 6 #LOWER THAN
    LOREQ = 7 #LOWER OR EQUAL
    EQ = 8 #EQUAL
    BOREQ = 9 #BIGGER OR EQUAL
    BT = 10 #BIGGER THAN
    DIFF = 11 #DIFFERENT THAN
    #SÍMBOLOS OPERACIONALES
    PLUS = 12
    MINUS = 13
    MULT = 14
    DIV = 15
    MOD = 16
    INC = 17
    DEC = 18
    #ASSIGN
    ASSIGN = 19
    #SEMICOLON
    SEMI = 20
    #PARENTHESIS
    OPENP = 21
    CLOSEP = 22
    # CONTAINER
    OPENC = 23
    CLOSEC = 24
    # COMMA
    COMMA = 25
    #PALABRAS RESERVADAS main, if, then, else, end, do, while, cin, cout, real, int, boolean
    MAIN = 31
    IF = 32
    THEN = 33
    ELSE = 34
    END = 35
    DO = 36
    WHILE = 37 
    UNTIL = 43 
    CIN = 38
    COUT = 39
    REAL = 40
    INT = 41
    BOOLEAN = 42
    #END OF FILE
    EOF = 200
    ERROR = 400

class STATE(enum.Enum):
    START = 0
    ID = 1
    PLUS = 2
    NUM = 3
    MINUS = 4
    DIAG = 5
    MINOR = 6
    BIGGER = 7
    EQUAL = 8
    NOT = 9
    ASSIGN = 10
    DOT = 11
    FLOAT = 12
    COMM_LINE = 13
    COMM_BLOCK = 14
    COMM_BLOCK_END = 15
    SPACES = 16
    UNIQUE = 17
    DONE = 200
    ERROR = 400
    EOF = 100

reservedWords = { 
    "main": TokenType.MAIN, 
    "if": TokenType.IF,
    "then" : TokenType.THEN, 
    "else" : TokenType.ELSE, 
    "end" : TokenType.END, 
    "do" : TokenType.DO, 
    "while" : TokenType.WHILE,
    "until":  TokenType.UNTIL,
    "cin" : TokenType.CIN, 
    "cout" : TokenType.COUT, 
    "real" : TokenType.REAL, 
    "int" : TokenType.INT, 
    "boolean" : TokenType.BOOLEAN
}

uniqueCharacter = {
    "*" : TokenType.MULT,
    "%" : TokenType.MOD,
    "(" : TokenType.OPENP,
    ")" : TokenType.CLOSEP,
    "{" : TokenType.OPENC,
    "}" : TokenType.CLOSEC,
    ";" : TokenType.SEMI,
    "," : TokenType.COMMA
}

startSimbol = {
    "+" : STATE.PLUS,
    "-" : STATE.MINUS,
    "/" : STATE.DIAG,
    "<" : STATE.MINOR,
    ">" : STATE.BIGGER,
    "=" : STATE.EQUAL,
    "!" : STATE.NOT,
    ":" : STATE.ASSIGN,
    " " : STATE.SPACES,
   "\t" : STATE.SPACES,
   "\n" : STATE.SPACES
}