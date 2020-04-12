from token import Token, getToken
from enumTypes import reserved, TokenType

tokens = []
while (True):
    token = getToken()
    tokens.append(token)
    if (token.type == TokenType.EOF):
        break

print (*tokens, sep = "\n")