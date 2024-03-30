class Jp2File:
    name: str
    band: str
    path: str

    def __init__(self, name: str, band: str, path: str):
        self.name = name
        self.band = band
        self.path = path

    def __str__(self):
        return f'[name: {self.name}] [band: {self.band}] [path:{self.path}]'
