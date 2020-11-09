class SDT:

    def __init__(self, data = '') -> None:
        self.data = data
        self.type = None
        self.val = None

    def __repr__(self):
        return repr(self.data)