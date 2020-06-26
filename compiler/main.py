import argparse
from lexic.lexicMain import Lex
from lexic.enumTypes import TokenType

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
parser.add_argument('-t', '--tracer', type=str2bool, nargs='?', const=True, default=False, help='tracer when executing lex only')
parser.add_argument('-D', '--debugg', type=str2bool, nargs='?', const=True, default=False, help='debugg for devs')
parser.add_argument('-l', '--lex', type=str2bool, nargs='?', const=True, default=False, help='lex only')
parser.add_argument('-o', '--output', default=None, help='personalized output file and directory')
requiredNamed = parser.add_argument_group('required named arguments')
requiredNamed.add_argument('-d', '--dir', help='main file directory', required=True)
requiredNamed.add_argument('-f', '--file', help='main file name', required=True)
args = parser.parse_args()

if args.debugg == True: 
    print("compiler is debugging") 
    lex = Lex("/home/beristain/Documents/uaa/compis", "pruebas.txt", args.tracer)
else: 
    lex = Lex(args.dir,args.file,args.tracer,args.output)

if args.lex:
    #tokens = lex.run()
    while True:
        token = lex.getToken()
        if token.type == TokenType.EOF:
            break
print("build: finshed")
