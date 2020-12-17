class Instruction:
    def __init__(self, operation=0, data=None, type=None)-> None:
        self.operation = operation
        self.data = data
        self.type = type