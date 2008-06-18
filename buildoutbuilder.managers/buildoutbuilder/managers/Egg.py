class Egg:
    def __init__(self,name,uri=None):
        self.name = name
        self.uri = uri

    def __repr__(self):
        return self.name
