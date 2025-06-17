class Playlist:
    def __init__(self, nome):
        self.nome = nome
        self.musicas = []

    def adicionar_musica(self, musica):
        self.musicas.append(musica)

    def remover_musica(self, musica):
        if musica in self.musicas:
            self.musicas.remove(musica)

    def listar(self):
        print(f"Playlist: {self.nome}")
        for i, m in enumerate(self.musicas, 1):
            print(f"{i}. {m}")
