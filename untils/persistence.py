import json
import os
from models.musica import Musica

DATA_FILE = "data/data.json"

def salvar_dados(player, playlists, favoritos, filepath=DATA_FILE):
    #Salva o estado da aplicação (fila, playlists, favoritos) em um arquivo JSON.
    dados = {
        "fila": [musica.to_dict() for musica in player.fila],
        "historico": [musica.to_dict() for musica in player.historico],
        "playlists": {
            nome: [musica.to_dict() for musica in musicas]
            for nome, musicas in playlists.items()
        },
        # Salva os caminhos dos arquivos favoritos
        "favoritos": list(favoritos)  
    }
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

def _criar_dados_padrao(music_dir="data"):
    #Cria uma estrutura de dados padrão com músicas da pasta 'data'.
    print(f"Arquivo de dados não encontrado. Criando um novo com músicas da pasta '{music_dir}'.")
    fila_padrao = []

    if os.path.exists(music_dir):
        for filename in os.listdir(music_dir):
            if filename.lower().endswith(('.mp3', '.wav', '.ogg')):
                filepath = os.path.join(music_dir, filename).replace("\\", "/")
                musica = Musica(
                    titulo=os.path.splitext(filename)[0],
                    artista="Desconhecido",
                    album="Desconhecido",
                    genero="Desconhecido",
                    caminho_arquivo=filepath
                )
                fila_padrao.append(musica)
    
    return {
        "fila": fila_padrao, 
        "historico": [], 
        "playlists": {}, 
        "favoritos": set()
    }

def carregar_dados(filepath=DATA_FILE):
    """Carrega o estado da aplicação de um arquivo JSON.
    Se o arquivo não existir, cria um com as músicas da pasta 'data'.
    """
    if not os.path.exists(filepath):
        return _criar_dados_padrao(os.path.dirname(filepath) or "data")

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            dados = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return _criar_dados_padrao(os.path.dirname(filepath) or "data")

    fila = [Musica.from_dict(m) for m in dados.get("fila", [])]
    historico = [Musica.from_dict(m) for m in dados.get("historico", [])]
    playlists = {
        nome: [Musica.from_dict(m) for m in musicas]
        for nome, musicas in dados.get("playlists", {}).items()
    }
    favoritos = set(dados.get("favoritos", []))

    return {"fila": fila, "historico": historico, "playlists": playlists, "favoritos": favoritos}
