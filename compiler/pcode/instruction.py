class Instruction:
    def __init__(self, operation=0, level=0, data=None)-> None:
        self.operation = operation
        self.level = level
        self.data = data