from abc import ABC, abstractmethod

class Command(ABC):
    """
    A interface Command declara um método para executar um comando.
    """
    @abstractmethod
    def execute(self):
        pass

class TogglePlayPauseCommand(Command):
    """Comando que alterna entre play e pause."""
    def __init__(self, player):
        self._player = player

    def execute(self):
        if self._player.esta_pausado:
            self._player.continuar()
        elif self._player.esta_reproduzindo:
            self._player.pausar()
        else:
            # Se não estiver tocando nada, inicia a fila
            self._player.iniciar_em_thread()

class NextCommand(Command):
    """Comando para tocar a próxima música."""
    def __init__(self, player):
        self._player = player

    def execute(self):
        self._player.proxima()

class PreviousCommand(Command):
    """Comando para tocar a música anterior."""
    def __init__(self, player):
        self._player = player

    def execute(self):
        self._player.anterior()

class TocarMusicaCommand(Command):
    """Comando para tocar uma música específica."""
    def __init__(self, player, musica):
        self._player = player
        self._musica = musica

    def execute(self):
        self._player.tocar(self._musica)