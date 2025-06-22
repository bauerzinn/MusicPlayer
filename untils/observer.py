
from abc import ABC, abstractmethod

class Subject(ABC):
    """
    A classe Subject (Sujeito) que pode ser observada.
    """
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        """Anexa um observador ao sujeito."""
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        """Desanexa um observador."""
        try:
            self._observers.remove(observer)
        except ValueError:
            pass

    def notify(self, event, data=None):
        """Notifica todos os observadores sobre um evento."""
        for observer in self._observers:
            observer.update(event, data)

class Observer(ABC):
    """
    A classe Observer (Observador) que reage a atualizações do sujeito.
    """
    @abstractmethod
    def update(self, event, data=None):
        """Recebe a atualização do sujeito."""
        pass