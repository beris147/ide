import sys, os
from machine import Machine

file = sys.argv[1]
machine = Machine(file)
machine.run()