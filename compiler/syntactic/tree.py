class Tree:
    def __init__(self, name='root', children=None):
        self.name = name
        self.children = []
        self.lineo = 
        
        if children is not None:
            for child in children:
                self.add_child(child)

    def __repr__(self):
        return self.name

    def add_child(self, node):
        assert isinstance(node, Tree)
        self.children.append(node)