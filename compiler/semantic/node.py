class SDT:

    def __init__(self, data = '', type = None, val = None) -> None:
        self.data = data
        self.type = type
        self.val = val

    def __repr__(self):
        
        # Only syntactic
        #return repr(self.data)

        # FIXME: Debug for semantic
        return str(dict(type=self.type, val=self.val, token=repr(self.data)))