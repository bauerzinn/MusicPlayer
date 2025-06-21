import pygame
import threading
from time import sleep

class Player:
    def __init__(self):
        pygame.mixer.init()
        self.musica_atual = None
        self.fila = []  # Lista de músicas para reprodução
        self.indice_atual = 0
        self.historico = []  # Pilha para histórico de músicas
        self.esta_reproduzindo = False
        self.thread = None
        self.parar_reproducao = False
        self.esta_pausado = False

    def adicionar_na_fila(self, musica):
        self.fila.append(musica)

    def iniciar_em_thread(self):
        if not self.thread or not self.thread.is_alive():
            self.parar_reproducao = False
            self.thread = threading.Thread(target=self._reproduzir_fila)
            self.thread.daemon = True
            self.thread.start()

    def _reproduzir_fila(self):
        while not self.parar_reproducao:
            if self.fila and not pygame.mixer.music.get_busy() and not self.esta_pausado:
                musica = self.fila.pop(0)
                if musica.existe_arquivo():
                    print(f"Reproduzindo: {musica}")
                    self.musica_atual = musica
                    self.historico.append(musica)  # Adiciona à história
                    pygame.mixer.music.load(musica.caminho_arquivo)
                    pygame.mixer.music.play()
                else:
                    print(f"Arquivo não encontrado: {musica.caminho_arquivo}")
            sleep(0.1)  # Evita uso excessivo de CPU

    def parar(self):
        self.parar_reproducao = True
        pygame.mixer.music.stop()
        if self.thread and self.thread.is_alive():
            self.thread.join()

    def pausar(self):
        self.esta_pausado = True
        pygame.mixer.music.pause()

    def continuar(self):
        self.esta_pausado = False
        pygame.mixer.music.unpause()

    def tocar(self, musica=None):
        if musica:
            try:
                self.indice_atual = self.fila.index(musica)
            except ValueError:
                return
        musica_atual = self.fila[self.indice_atual]
        # Adiciona ao histórico antes de tocar
        if not self.historico or self.historico[-1] != musica_atual:
            self.historico.append(musica_atual)
        pygame.mixer.music.load(musica_atual.caminho_arquivo)
        pygame.mixer.music.play()

    def proxima(self):
        if self.indice_atual < len(self.fila) - 1:
            self.indice_atual += 1
            self.tocar()
    
    def anterior(self):
        if self.indice_atual > 0:
            self.indice_atual -= 1
            self.tocar()
        elif self.historico:
            # Volta para a última música do histórico
            ultima = self.historico.pop()
            self.tocar(ultima)
        else:
            print("Não há música anterior para tocar")

    def volume(self, nivel):
        pygame.mixer.music.set_volume(nivel)

    def get_musica_atual(self):
        return self.musica_atual

    def ver_historico(self):
        return list(reversed(self.historico))
