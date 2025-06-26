from abc import ABC, abstractmethod

class Command(ABC):

    @abstractmethod
    def execute(self):
        pass

class TogglePlayPauseCommand(Command):
    def __init__(self, player):
        self._player = player

    def execute(self):
        if self._player.esta_pausado:
            self._player.continuar()
        elif self._player.esta_reproduzindo:
            self._player.pausar()
        else:
            self._player.iniciar_em_thread()

class NextCommand(Command):
    def __init__(self, player):
        self._player = player

    def execute(self):
        self._player.proxima()

class PreviousCommand(Command):
    def __init__(self, player):
        self._player = player

    def execute(self):
        self._player.anterior()

class TocarMusicaCommand(Command):
    def __init__(self, player, musica):
        self._player = player
        self._musica = musica

    def execute(self):
        self._player.tocar(self._musica)