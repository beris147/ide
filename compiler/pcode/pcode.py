import sys, os
from machine import Machine

#file = sys.argv[1]
machine = Machine("/home/beristain/Documents/uaa/compis/problemas/compilador/pcode.o")
#machine = Machine(file)
machine.run()

input("Press enter to continue...")