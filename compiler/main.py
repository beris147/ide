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
"""
parser = argparse.ArgumentParser(description='tiny lexical analyzer')
parser.add_argument('-D', '--debugg', type=str2bool, nargs='?', const=True, default=False, help='debugg for devs')
parser.add_argument('-p', '--parser', type=str2bool, nargs='?', const=True, default=False, help='false for an only lexical compiler')
parser.add_argument('-a', '--analyze', type=str2bool, nargs='?', const=True, default=False, help='false for an only syntactic compiler')
parser.add_argument('-o', '--output', default=None, help='personalized output file and directory')
parser.add_argument('-s', '--traceScan', type=str2bool, nargs='?', const=True, default=False, help='print the scan')
requiredNamed = parser.add_argument_group('required named arguments')
requiredNamed.add_argument('-d', '--dir', help='main file directory', required=True)
requiredNamed.add_argument('-f', '--file', help='main file name', required=True)
args = parser.parse_args()

if args.debugg == True: 
    print("compiler is debugging") 
    lex = Lex("/home/beristain/Documents/uaa/compis", "pruebas.txt", args.traceScan)
else: 
    lex = Lex(args.dir,args.file,args.traceScan,args.output)

if args.parser == False:
    #tokens = lex.run()
    while True:
        token = lex.getToken()
        if token.type == TokenType.EOF:
            break
else:
    parser = Parser(lex)
    parser.parse()
"""
lex = Lex("/home/beristain/Documents/uaa/compis", "pruebas.txt", False)
parser = Parser(lex)
parser.parse()
#"""
print("build: finshed")