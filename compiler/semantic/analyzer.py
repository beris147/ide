from enumTypes import TokenType
from .symtab import SymTable
from lexic.token import Token
from syntactic.tree import ATS
from typing import Callable

class Analyzer:

    def __init__(self, tree: ATS) -> None:
        self.tree = tree
        self.symtab = SymTable()

        self.tree.traverse(self.symtab)
