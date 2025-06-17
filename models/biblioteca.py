from models.musica import Musica

class BibliotecaMusical:
    def __init__(self):
        self.musicas = []

    def adicionar_musica(self, musica: Musica):
        self.musicas.append(musica)

    def buscar_por_artista(self, artista):
        return [m for m in self.musicas if m.artista.lower() == artista.lower()]

    def listar_musicas(self):
        for i, m in enumerate(self.musicas, start=1):
            print(f"{i}. {m}")
