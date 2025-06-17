import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pygame
from tkinter import filedialog
from models.musica import Musica

class InterfaceMusical:
    def __init__(self, player):
        self.player = player
        self.root = tk.Tk()
        self.root.title("Music Player")
        self.root.geometry("1500x600")
        self.root.configure(bg="#232323")

        # Barra lateral
        sidebar = tk.Frame(self.root, bg="#232323", width=70)
        sidebar.pack(side="left", fill="y")
        for icon in ["home", "playlist", "heart", "repeat", "settings"]:
            btn = tk.Button(sidebar, text=" ", bg="#232323", relief="flat", bd=0, highlightthickness=0, activebackground="#232323")
            btn.pack(pady=10, padx=0, fill="x")

        # Área principal
        main_area = tk.Frame(self.root, bg="#232323")
        main_area.pack(side="left", fill="both", expand=True)

        # Topo: título e busca
        top_frame = tk.Frame(main_area, bg="#232323")
        top_frame.pack(fill="x", pady=10)
        tk.Label(top_frame, text="Library", fg="white", bg="#232323", font=("Consolas", 22, "bold")).pack(side="left", padx=20)
        tk.Entry(top_frame, width=30, font=("Segoe UI", 12), bg="#fff", relief="flat").pack(side="right", padx=20)

        # Grid de músicas
        grid_frame = tk.Frame(main_area, bg="#232323")
        grid_frame.pack(fill="both", expand=True, padx=20, pady=(0, 0))
        self._criar_grid_musicas(grid_frame)

        # Lado direito (controles e info)
        right_frame = tk.Frame(self.root, bg="#232323", width=400)
        right_frame.pack(side="left", fill="both", expand=True)

        # Botão Adicionar Música
        self.botao_adicionar = tk.Button(right_frame, text="＋ Adicionar Música", font=("Segoe UI", 12), bg="#292929", fg="white", relief="flat", activebackground="#444")
        self.botao_adicionar.pack(side="top", fill="x", padx=30, pady=(10, 0))
        self.botao_adicionar.config(command=self._adicionar_musica)

        # Espaço para centralizar controles na parte inferior
        right_frame.grid_rowconfigure(0, weight=1)
        right_frame.grid_rowconfigure(1, weight=1)
        right_frame.grid_rowconfigure(2, weight=1)
        right_frame.grid_rowconfigure(3, weight=1)
        right_frame.grid_rowconfigure(4, weight=1)
        right_frame.grid_rowconfigure(5, weight=1)
        right_frame.grid_rowconfigure(6, weight=1)
        right_frame.grid_rowconfigure(7, weight=1)
        right_frame.grid_rowconfigure(8, weight=1)
        right_frame.grid_rowconfigure(9, weight=1)
        right_frame.grid_rowconfigure(10, weight=1)

        # Volume e controles na parte inferior
        bottom_controls = tk.Frame(right_frame, bg="#232323")
        bottom_controls.pack(side="bottom", fill="x", pady=30)

        # Volume
        volume_frame = tk.Frame(bottom_controls, bg="#232323")
        volume_frame.pack(side="top", anchor="w", pady=(0, 10))
        tk.Label(volume_frame, text="🔊 Volume", bg="#232323", fg="white", font=("Segoe UI", 11)).pack(side="left", padx=(0, 10))
        self.volume_scale = ttk.Scale(volume_frame, from_=0, to=1, orient=tk.HORIZONTAL, command=self._ajustar_volume, length=150)
        self.volume_scale.set(0.5)
        self.volume_scale.pack(side="left")

        # Controles agrupados e centralizados
        controls_frame = tk.Frame(bottom_controls, bg="#232323")
        controls_frame.pack(side="top", pady=10)

        self.botao_anterior = tk.Button(controls_frame, text="⏮ Anterior", font=("Segoe UI", 11), bg="#292929", fg="white", relief="flat", width=12, activebackground="#444", activeforeground="white", command=self._anterior)
        self.botao_anterior.pack(side="left", padx=10)

        self.botao_play_pause = tk.Button(controls_frame, text="▶ Play", font=("Segoe UI", 11), bg="#292929", fg="white", relief="flat", width=12, activebackground="#444", activeforeground="white", command=self._play_pause)
        self.botao_play_pause.pack(side="left", padx=10)

        self.botao_proximo = tk.Button(controls_frame, text="Próximo ⏭", font=("Segoe UI", 11), bg="#292929", fg="white", relief="flat", width=12, activebackground="#444", activeforeground="white", command=self._proximo)
        self.botao_proximo.pack(side="left", padx=10)

        self.botao_parar = tk.Button(controls_frame, text="⏹ Parar", font=("Segoe UI", 11), bg="#292929", fg="white", relief="flat", width=12, activebackground="#444", activeforeground="white", command=self._parar)
        self.botao_parar.pack(side="left", padx=10)

        # Informações da música (opcional, pode remover se não quiser)
        info_frame = tk.Frame(right_frame, bg="#232323")
        info_frame.pack(side="top", fill="x", pady=20)
        self.titulo_label = tk.Label(info_frame, text="", bg="#232323", fg="white", font=("Segoe UI", 16, "bold"))
        self.titulo_label.pack(side="left", padx=10)
        self.artista_label = tk.Label(info_frame, text="", bg="#232323", fg="#bbbbbb", font=("Segoe UI", 12))
        self.artista_label.pack(side="left", padx=10)

        self._atualizar_musica()
        self.root.mainloop()

    def _atualizar_musica(self):
        musica = self.player.get_musica_atual()
        if musica:
            self.titulo_label['text'] = musica.titulo
            self.artista_label['text'] = musica.artista
        else:
            self.titulo_label['text'] = ""
            self.artista_label['text'] = ""
        self.root.after(1000, self._atualizar_musica)

    def _play_pause(self):
        if pygame.mixer.music.get_busy():
            self.player.pausar()
            self.botao_play_pause.configure(text="▶ Play")
        else:
            self.player.continuar()
            self.botao_play_pause.configure(text="⏸ Pausar")

    def _anterior(self):
        self.player.anterior()
        self._atualizar_musica()

    def _proximo(self):
        self.player.proxima()
        self._atualizar_musica()

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
        # Atualize o grid de músicas após adicionar
        self._criar_grid_musicas(self.root.winfo_children()[1].winfo_children()[2])

    def _criar_grid_musicas(self, parent):
        # Limpa o grid antes de recriar
        for widget in parent.winfo_children():
            widget.destroy()

        musicas = self.player.fila
        colunas = 4
        card_width = 220
        card_height = 240
        img_size = 160

        for idx, musica in enumerate(musicas):
            i = idx // colunas
            j = idx % colunas
            card = tk.Frame(parent, bg="#292929", width=card_width, height=card_height)
            card.grid(row=i, column=j, padx=25, pady=20)
            card.pack_propagate(False)  # Impede o frame de se ajustar ao conteúdo

            img = Image.new("RGB", (img_size, img_size), color="#444")
            img_tk = ImageTk.PhotoImage(img)
            lbl_img = tk.Label(card, image=img_tk, bg="#292929", width=img_size, height=img_size)
            lbl_img.image = img_tk
            lbl_img.pack(pady=(10, 5))

            tk.Label(card, text=musica.titulo, fg="white", bg="#292929", font=("Segoe UI", 11, "bold")).pack()
            tk.Label(card, text=musica.artista, fg="#bbbbbb", bg="#292929", font=("Segoe UI", 10)).pack()

            card.bind("<Button-1>", lambda e, m=musica: self._tocar_musica(m))
            for child in card.winfo_children():
                child.bind("<Button-1>", lambda e, m=musica: self._tocar_musica(m))

    def _tocar_musica(self, musica):
        self.player.tocar(musica)
        self._atualizar_musica()
