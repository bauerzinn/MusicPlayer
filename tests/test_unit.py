import unittest
from unittest.mock import MagicMock, patch
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.musica import Musica
from player.player import Player

class TestMusica(unittest.TestCase):
    def test_criar_musica(self):
        musica = Musica(
            titulo="Bohemian Rhapsody",
            artista="Queen",
            album="A Night at the Opera",
            genero="Rock",
            caminho_arquivo="/path/to/bohemian.mp3"
        )
        self.assertEqual(musica.titulo, "Bohemian Rhapsody")
        self.assertEqual(musica.artista, "Queen")
        self.assertEqual(musica.album, "A Night at the Opera")
        self.assertEqual(musica.genero, "Rock")
        self.assertEqual(musica.caminho_arquivo, "/path/to/bohemian.mp3")



@patch('player.player.pygame')
class TestPlayer(unittest.TestCase):
    def setUp(self):

        self.player = Player()
        self.musica1 = Musica("Musica 1", "Artista 1", "Album 1", "Pop", "path/1.mp3")
        self.musica2 = Musica("Musica 2", "Artista 2", "Album 2", "Rock", "path/2.mp3")
        self.player.adicionar_na_fila(self.musica1)
        self.player.adicionar_na_fila(self.musica2)

    def test_adicionar_na_fila(self, mock_pygame):
        """Testa se as músicas são adicionadas corretamente à fila."""
        self.assertEqual(len(self.player.fila), 2)
        self.assertEqual(self.player.fila[0].titulo, "Musica 1")

    def test_tocar_musica(self, mock_pygame):
        """Testa se a música correta é tocada e adicionada ao histórico."""
        self.player.tocar(self.musica1)
        self.assertFalse(self.player.esta_pausado)
        self.assertEqual(self.player.musica_atual, self.musica1)
        self.assertIn(self.musica1, self.player.historico)
        mock_pygame.mixer.music.load.assert_called_with("path/1.mp3")
        mock_pygame.mixer.music.play.assert_called_once()

    def test_pausar_e_continuar(self, mock_pygame):
        """Testa a funcionalidade de pausar e continuar a música."""
        self.player.tocar(self.musica1)
        
        self.player.pausar()
        self.assertTrue(self.player.esta_pausado)
        mock_pygame.mixer.music.pause.assert_called_once()

        self.player.continuar()
        self.assertFalse(self.player.esta_pausado)
        mock_pygame.mixer.music.unpause.assert_called_once()

    def test_proxima(self, mock_pygame):
        """Testa se o player avança para a próxima música."""
        self.player.tocar(self.musica1)
        self.player.proxima()
        self.assertEqual(self.player.musica_atual, self.musica2)
        self.assertFalse(self.player.esta_pausado)
        mock_pygame.mixer.music.load.assert_called_with("path/2.mp3")

    def test_anterior(self, mock_pygame):
        """Testa se o player volta para a música anterior."""
        self.player.tocar(self.musica2)
        self.player.anterior()
        self.assertEqual(self.player.musica_atual, self.musica1)
        self.assertFalse(self.player.esta_pausado)
        mock_pygame.mixer.music.load.assert_called_with("path/1.mp3")

    def test_proxima_no_fim_da_fila(self, mock_pygame):
        """Testa se o player não faz nada ao tentar avançar no fim da fila."""
        self.player.tocar(self.musica2)
        # O teste verifica se o estado não muda de forma inesperada.
        self.player.proxima()
        self.assertEqual(self.player.musica_atual, self.musica2) # Deve permanecer na última música
        self.assertFalse(self.player.esta_pausado)

if __name__ == '__main__':
    unittest.main()
