import argparse
import lexicFiles.variables as var
from lexicFiles.lexicMain import Lexer

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
parser.add_argument('-t', '--tracer', type=str2bool, nargs='?', const=True, default=False, help='tracer scan required')
parser.add_argument('-o', '--output', default=None, help='personalized output file and directory')
requiredNamed = parser.add_argument_group('required named arguments')
requiredNamed.add_argument('-d', '--dir', help='main file directory', required=True)
requiredNamed.add_argument('-f', '--file', help='main file name', required=True)
args = parser.parse_args()

""" OLD METHOD
var.init(args.dir,args.file,args.tracer,args.output)
startLexicAnalysis() #Lexic Analysis
if var.TraceScan:   
    var.output.close()
    """
lex = Lexer(args.dir,args.file,args.tracer,args.output)
# for debugging + lex = Lexer("C:\\Users\\beris\\OneDrive\\Escritorio", "main.txt", True)
tokens = lex.run()
print("build: finshed")