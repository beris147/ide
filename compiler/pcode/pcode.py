import sys, os
from machine import Machine

file = sys.argv[1]
#machine = Machine("/home/beristain/Documents/uaa/compis/compilador/pcode.o")
machine = Machine(file)
machine.run()