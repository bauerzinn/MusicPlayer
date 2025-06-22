
class LibraryOrganizer:
    """
    Organiza a biblioteca de músicas em uma estrutura hierárquica (árvore).
    A estrutura é: Gênero -> Artista -> Álbum -> [Músicas]
    """
    def build_tree(self, musicas):
        """
        Constrói uma árvore hierárquica a partir de uma lista de músicas.

        Args:
            musicas (list): Uma lista de objetos Musica.

        Returns:
            dict: Um dicionário aninhado representando a árvore.
        """
        tree = {}
        for musica in musicas:
            # Garante que valores nulos ou vazios sejam tratados
            genero = musica.genero if musica.genero else "Gênero Desconhecido"
            artista = musica.artista if musica.artista else "Artista Desconhecido"
            album = musica.album if musica.album else "Álbum Desconhecido"

            if genero not in tree:
                tree[genero] = {}
            
            if artista not in tree[genero]:
                tree[genero][artista] = {}
                
            if album not in tree[genero][artista]:
                tree[genero][artista][album] = []
                
            tree[genero][artista][album].append(musica)
            
        return tree