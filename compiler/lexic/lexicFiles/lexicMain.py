from .token import Token, getToken
from .enumTypes import reservedWords, TokenType

def startLexicAnalysis():
    tokens = []
    while (True):
        token = getToken()
        tokens.append(token)
        if (token.type == TokenType.EOF):
            break
    print(*tokens)