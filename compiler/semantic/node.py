class SDT(dict):

    def __init__(self, data = '', type = None, val = None, lineo = None, token = None) -> None:
        self.__dict__ = self
        self.data = data
        self.type = type
        self.val = val
        self.lineo = lineo
        self.token = token

    # def __repr__(self):
        
    #     # Only syntactic
    #     return repr(self.data)

    #     # FIXME: Debug for semantic
    #     #return str(dict(type=self.type, val=self.val, data=repr(self.data),lineo=self.lineo,token=self.token))