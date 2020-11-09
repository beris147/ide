import argparse
from lexic.lex import Lex
from enumTypes import TokenType
from syntactic.parser import Parser

def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

parser = argparse.ArgumentParser(description='tiny lexical analyzer')
parser.add_argument('-D', '--debugg', type=str2bool, nargs='?', const=True, default=False, help='debugg for devs')
parser.add_argument('-p', '--parser', type=str2bool, nargs='?', const=True, default=False, help='false for an only lexical compiler')
parser.add_argument('-a', '--analyze', type=str2bool, nargs='?', const=True, default=False, help='false for an only syntactic compiler')
parser.add_argument('-S', '--traceScan', type=str2bool, nargs='?', const=True, default=False, help='print the scan tokens')
parser.add_argument('-P', '--traceParser', type=str2bool, nargs='?', const=True, default=False, help='print the syntactic tree')
requiredNamed = parser.add_argument_group('required named arguments')
requiredNamed.add_argument('-d', '--dir', help='main file directory', required=True)
requiredNamed.add_argument('-f', '--file', help='main file name', required=True)
args = parser.parse_args()

dir = ""
file = ""

if args.debugg == True: 
    print("compiler is debugging") 
    dir = "/home/beristain/Documents/uaa/compis"
    file = "pruebas.txt"
else: 
    dir = args.dir
    file = args.file

lex = Lex(dir, file, args.traceScan)

if args.parser == False:
    while True:
        token = lex.getToken()
        if token.type == TokenType.EOF:
            break
else:
    parser = Parser(lex, dir, args.traceParser)
    parser.parse()
"""
lex = Lex("/home/beristain/Documents/uaa/compis", "pruebas.txt", True)
parser = Parser(lex, "/home/beristain/Documents/uaa/compis", True)
parser.parse()
#"""
print("build: finshed")