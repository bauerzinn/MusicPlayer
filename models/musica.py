import os

class Musica:
    def __init__(self, titulo, artista, album, genero, caminho_arquivo):
        self.titulo = titulo
        self.artista = artista
        self.album = album
        self.genero = genero
        self.caminho_arquivo = caminho_arquivo

    def to_dict(self):
        return {
            "titulo": self.titulo,
            "artista": self.artista,
            "album": self.album,
            "genero": self.genero,
            "caminho_arquivo": self.caminho_arquivo,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    def __str__(self):
        return f"{self.titulo} - {self.artista} ({self.album})"
    
    def existe_arquivo(self):
        return os.path.exists(self.caminho_arquivo)
