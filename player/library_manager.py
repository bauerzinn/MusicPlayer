import os
import mutagen
from tkinter import filedialog, messagebox
from models.musica import Musica
from player.libraryOrganizer import LibraryOrganizer

class LibraryManager:
    def __init__(self, player):
        self.player = player
        # A biblioteca principal de músicas será a fila do player
        self.biblioteca = self.player.fila
        self.organizer = LibraryOrganizer()
        self.organized_library = self.organizer.build_tree(self.biblioteca)

    def adicionar_musica(self):
        caminho_arquivo = filedialog.askopenfilename(
            title="Selecionar música",
            filetypes=[("Arquivos de Áudio", "*.mp3 *.wav *.ogg")]
        )
        if not caminho_arquivo:
            return None

        try:
            audio = mutagen.File(caminho_arquivo, easy=True)
            titulo = audio.get('title', [os.path.basename(caminho_arquivo)])[0]
            artista = audio.get('artist', ['Desconhecido'])[0]
            album = audio.get('album', ['Desconhecido'])[0]
            genero = audio.get('genre', ['Desconhecido'])[0]

            nova_musica = Musica(titulo, artista, album, genero, caminho_arquivo)
            self.biblioteca.append(nova_musica)
            self.reorganize_library()
            return nova_musica

        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível ler os metadados do arquivo: {e}")
            return None

    def reorganize_library(self):
        """Reconstrói a árvore da biblioteca."""
        self.organized_library = self.organizer.build_tree(self.biblioteca)

    def buscar_musicas(self, termo, musicas):
        termo = termo.lower()
        if not termo:
            return musicas

        return [
            m for m in musicas
            if termo in m.titulo.lower()
            or termo in m.artista.lower()
            or termo in m.genero.lower()
            or termo in m.album.lower()
        ]

    def ordenar_musicas(self, criterio, musicas):
        criterio = criterio.lower()
        if criterio == "título":
            musicas.sort(key=lambda m: m.titulo)
        elif criterio == "artista":
            musicas.sort(key=lambda m: m.artista)
        elif criterio == "gênero":
            musicas.sort(key=lambda m: m.genero)
        elif criterio == "álbum":
            musicas.sort(key=lambda m: m.album)
        return musicas
