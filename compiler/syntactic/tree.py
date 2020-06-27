class Tree:
    def __init__(self, token = None, lineo = None, children=None):
        self.token = token
        self.children = []
        self.lineo = lineo
        
        if children is not None:
            for child in children:
                self.add_child(child)

    def __repr__(self):
        return self.token

    def add_child(self, node):
        assert isinstance(node, Tree)
        self.children.append(node)