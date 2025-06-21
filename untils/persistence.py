import json
import os
from models.musica import Musica

DATA_FILE = "data/data.json"

def salvar_dados(player, playlists, favoritos):
    """Salva o estado da aplicação (fila, playlists, favoritos) em um arquivo JSON."""
    dados = {
        "fila": [musica.to_dict() for musica in player.fila],
        "historico": [musica.to_dict() for musica in player.historico],
        "playlists": {
            nome: [musica.to_dict() for musica in musicas]
            for nome, musicas in playlists.items()
        },
        "favoritos": list(favoritos)  # Salva os caminhos dos arquivos favoritos
    }
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

def carregar_dados():
    """Carrega o estado da aplicação de um arquivo JSON."""
    if not os.path.exists(DATA_FILE):
        return {"fila": [], "historico": [], "playlists": {}, "favoritos": set()}

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            dados = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {"fila": [], "historico": [], "playlists": {}, "favoritos": set()}

    # Converte dicionários de volta para objetos Musica
    fila = [Musica.from_dict(m) for m in dados.get("fila", [])]
    historico = [Musica.from_dict(m) for m in dados.get("historico", [])]
    playlists = {
        nome: [Musica.from_dict(m) for m in musicas]
        for nome, musicas in dados.get("playlists", {}).items()
    }
    favoritos = set(dados.get("favoritos", []))

    return {"fila": fila, "historico": historico, "playlists": playlists, "favoritos": favoritos}
