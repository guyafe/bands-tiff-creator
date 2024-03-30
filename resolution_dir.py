class ResolutionDir:
    name: str
    path: str

    def __init__(self, name: str, path: str):
        self.name = name
        self.path = path

    def __str__(self):
        return f'[name: {self.name}] [path:{self.path}]'
