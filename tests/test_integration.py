import unittest
import os
import json
import sys

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from untils.persistence import salvar_dados, carregar_dados
from models.musica import Musica
from player.player import Player

class TestPersistence(unittest.TestCase):
    def setUp(self):
        """Prepara o ambiente de teste."""
        self.player = Player()
        self.musica1 = Musica("Musica 1", "Artista 1", "Album 1", "Pop", "path/1.mp3")
        self.musica2 = Musica("Musica 2", "Artista 2", "Album 2", "Rock", "path/2.mp3")
        self.player.adicionar_na_fila([self.musica1, self.musica2])
        self.playlists = {"Minha Playlist": [self.musica1]}
        self.favoritos = {self.musica2.caminho_arquivo}
        self.arquivo_teste = "test_data.json"

    def tearDown(self):
        """Limpa o ambiente após o teste."""
        if os.path.exists(self.arquivo_teste):
            os.remove(self.arquivo_teste)

    def test_salvar_e_carregar_dados(self):
        """Testa se os dados são salvos e carregados corretamente."""
        # Salvar os dados
        salvar_dados(self.player, self.playlists, self.favoritos, self.arquivo_teste)

        # Verificar se o arquivo foi criado
        self.assertTrue(os.path.exists(self.arquivo_teste))

        # Carregar os dados
        dados_carregados = carregar_dados(self.arquivo_teste)

        # Verificar se os dados foram carregados corretamente
        self.assertEqual(len(dados_carregados["fila"]), 2)
        self.assertEqual(dados_carregados["fila"][0]['titulo'], "Musica 1")
        self.assertEqual(len(dados_carregados["playlists"]["Minha Playlist"]), 1)
        self.assertIn("path/2.mp3", dados_carregados["favoritos"])
        self.assertEqual(len(dados_carregados["historico"]), 0) # Histórico não é salvo neste fluxo

if __name__ == '__main__':
    unittest.main()
