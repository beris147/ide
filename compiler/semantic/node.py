class SDT:

    def __init__(self, data = '') -> None:
        self.data = data
        self.type = None
        self.val = None

    def __repr__(self):
        # Only syntactic
        # return repr(self.data)

        # FIXME: Debug for semantic
        return str(dict(type=self.type, val=self.val, token=repr(self.data)))