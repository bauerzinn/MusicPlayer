from models.musica import Musica
from models.biblioteca import BibliotecaMusical
from player.player import Player
from interface import InterfaceMusical

# Inicializar player e biblioteca
biblioteca = BibliotecaMusical()
player = Player()

# Adicionar músicas à biblioteca
musica1 = Musica(
    titulo="Make It Bun Dem",
    artista="Skrillex",
    album="Álbum Y",
    genero="Eletronica",
    caminho_arquivo="data/Skrillex Jr.  Make It Bun Dem.mp3"
)

musica2 = Musica(
    titulo="First of the Year (Equinox) Extended",
    artista="Skrillex",
    album="Álbum Y",
    genero="Eletronica",
    caminho_arquivo="data/Skrillex - First of the Year (Equinox) Extended.mp3"
)

musica3 = Musica(
    titulo="Exaltasamba - Um Minuto",
    artista="Exaltasamba",
    album="Álbum Y",
    genero="Samba",
    caminho_arquivo="data/exaltasamba - Um Minuto.mp3"
)

musica4 = Musica(
    titulo="Buque de Flores",
    artista="Exaltasamba",
    album="Álbum Y",
    genero="Samba",
    caminho_arquivo="data/Thiaguinho - Buque de Flores.mp3"
)

biblioteca.adicionar_musica(musica1)
biblioteca.adicionar_musica(musica2)
biblioteca.adicionar_musica(musica3)
biblioteca.adicionar_musica(musica4)

# Adicionar músicas à fila de reprodução
player.adicionar_na_fila(musica1)
player.adicionar_na_fila(musica2)
player.adicionar_na_fila(musica3)
player.adicionar_na_fila(musica4)

# Iniciar reprodução
player.iniciar_em_thread()

# Iniciar interface gráfica
InterfaceMusical(player)
