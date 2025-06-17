import tkinter as tk
from tkinter import ttk
import pygame
from tkinter import filedialog
from models.musica import Musica  # Certifique-se de importar sua classe Musica

class InterfaceMusical:
    def __init__(self, player):
        self.player = player
        self.root = tk.Tk()
        self.root.title("Reprodutor Musical")
        self.root.geometry("650x300")
        self.root.configure(bg="#1e1e1e")

        # Estilo
        style = ttk.Style()
        style.theme_use('clam')

        style.configure('TFrame', background='#1e1e1e')
        style.configure('TLabel', background='#1e1e1e', foreground='white', font=('Segoe UI', 11))
        style.configure('Titulo.TLabel', font=('Segoe UI', 16, 'bold'), foreground='#ff3c38')
        style.configure('TButton',
                        font=('Segoe UI', 11),
                        padding=10,
                        relief="flat",
                        background="#2e2e2e",
                        foreground="white")
        style.map('TButton',
                  background=[('active', '#ff3c38')],
                  foreground=[('active', 'white')])

        style.configure('TScale',
                        background='#1e1e1e',
                        troughcolor='#2e2e2e',
                        sliderlength=20)

        # Frame principal
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Informações da música
        self.info_frame = ttk.Frame(self.main_frame)
        self.info_frame.grid(row=0, column=0, columnspan=5, pady=20)

        self.titulo_label = ttk.Label(self.info_frame, text="", style='Titulo.TLabel')
        self.titulo_label.grid(row=0, column=0, padx=10)

        self.artista_label = ttk.Label(self.info_frame, text="", font=('Segoe UI', 12), foreground='#bbbbbb')
        self.artista_label.grid(row=1, column=0, padx=10)

        # Controles
        self.botao_anterior = ttk.Button(self.main_frame, text="⏮ Anterior", command=self._anterior)
        self.botao_anterior.grid(row=1, column=0, padx=10)

        self.botao_play_pause = ttk.Button(self.main_frame, text="▶ Play", command=self._play_pause)
        self.botao_play_pause.grid(row=1, column=1, padx=10)

        self.botao_proximo = ttk.Button(self.main_frame, text="Próximo ⏭", command=self._proximo)
        self.botao_proximo.grid(row=1, column=2, padx=10)

        self.botao_parar = ttk.Button(self.main_frame, text="⏹ Parar", command=self._parar)
        self.botao_parar.grid(row=1, column=3, padx=10)

        # Volume
        self.volume_frame = ttk.Frame(self.main_frame)
        self.volume_frame.grid(row=2, column=0, columnspan=5, pady=30)

        self.volume_label = ttk.Label(self.volume_frame, text="🔊 Volume")
        self.volume_label.grid(row=0, column=0, padx=10)

        self.volume_scale = ttk.Scale(self.volume_frame, from_=0, to=1, orient=tk.HORIZONTAL,
                                      command=self._ajustar_volume)
        self.volume_scale.set(0.5)
        self.volume_scale.grid(row=0, column=1, padx=10, ipadx=200)

        # Botão Adicionar Música
        self.botao_adicionar = ttk.Button(self.main_frame, text="➕ Adicionar Música", command=self._adicionar_musica)
        self.botao_adicionar.grid(row=3, column=0, columnspan=4, pady=10)

        # Menu de organização
        self.criterios = ["Artista", "Álbum", "Gênero", "Título"]
        self.criterio_var = tk.StringVar(value=self.criterios[0])
        self.menu_organizacao = ttk.OptionMenu(
            self.main_frame, self.criterio_var, self.criterios[0], *self.criterios, command=self._organizar_musicas
        )
        self.menu_organizacao.grid(row=4, column=0, columnspan=4, pady=10)

        # Lista de reprodução
        self.lista_reproducao = tk.Listbox(self.main_frame, bg="#2e2e2e", fg="white", font=('Segoe UI', 11), selectbackground="#ff3c38")
        self.lista_reproducao.grid(row=5, column=0, columnspan=4, sticky="ew", pady=10)

        # Atualizar música atual e lista de reprodução
        self._atualizar_musica()
        self._atualizar_lista_reproducao()
        self.root.mainloop()

    def _atualizar_musica(self):
        musica = self.player.get_musica_atual()
        if musica:
            self.titulo_label['text'] = musica.titulo
            self.artista_label['text'] = musica.artista
        self.root.after(1000, self._atualizar_musica)

    def _play_pause(self):
        if pygame.mixer.music.get_busy():
            self.player.pausar()
            self.botao_play_pause.configure(text="▶ Play")
        else:
            self.player.continuar()
            self.botao_play_pause.configure(text="⏸ Pausar")

    def _anterior(self):
        self.player.musica_anterior()
        self._atualizar_musica()
        self._atualizar_lista_reproducao()

    def _proximo(self):
        self.player.proxima_musica()
        self._atualizar_musica()
        self._atualizar_lista_reproducao()

    def _parar(self):
        self.player.parar()
        self.botao_play_pause.configure(text="▶ Play")

    def _ajustar_volume(self, valor):
        self.player.volume(float(valor))

    def _adicionar_musica(self):
        arquivos = filedialog.askopenfilenames(
            title="Selecione arquivos de música",
            filetypes=[("Arquivos de Áudio", "*.mp3 *.wav *.ogg")]
        )
        for arquivo in arquivos:
            nova_musica = Musica(
                titulo=arquivo.split("/")[-1],
                artista="Desconhecido",
                album="Desconhecido",
                genero="Desconhecido",
                caminho_arquivo=arquivo
            )
            self.player.adicionar_na_fila(nova_musica)
        self._atualizar_lista_reproducao()

    def _organizar_musicas(self, criterio):
        if criterio == "Artista":
            self.player.fila.sort(key=lambda m: m.artista)
        elif criterio == "Álbum":
            self.player.fila.sort(key=lambda m: m.album)
        elif criterio == "Gênero":
            self.player.fila.sort(key=lambda m: m.genero)
        elif criterio == "Título":
            self.player.fila.sort(key=lambda m: m.titulo)
        self._atualizar_lista_reproducao()

    def _atualizar_lista_reproducao(self):
        self.lista_reproducao.delete(0, tk.END)
        for musica in self.player.fila:
            self.lista_reproducao.insert(tk.END, f"{musica.titulo} - {musica.artista}")
