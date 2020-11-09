from enumTypes import TokenType
from .symtab import SymTable
from lexic.token import Token
from syntactic.tree import Tree
from typing import Callable

class Analyzer:

    def __init__(self, tree: Tree) -> None:
        self.tree = tree

    def traverse(self, root: Tree) -> None:
        for child in root.children:
            # TODO: function
            self.traverse(child)
