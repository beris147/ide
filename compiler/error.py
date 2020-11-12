class Error():
    def __init__(self, type='', message='', lineo='', col = None):
        self.type = type
        self.message = message
        self.lineo = lineo
        self.col = col

    def __repr__(self):
        strcol = f' col {self.col}' if self.col is not None else ''
        return '>>>{} error at line {}{}: {}'.format(self.type,self.lineo,strcol,self.message)