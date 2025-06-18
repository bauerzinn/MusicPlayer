import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from PIL import Image, ImageTk
import pygame
from tkinter import filedialog
from models.musica import Musica

class InterfaceMusical:
    def __init__(self, player):
        self.player = player
        self.favoritos = set()
        self.modo_favoritos = False
        self.modo_playlists = False
        self.playlists = {}  # nome: [Musica, Musica, ...]

        self.root = tk.Tk()
        self.root.title("Music Player")
        self.root.geometry("1500x650")
        self.root.configure(bg="#232323")

        # Topo: Navegação e busca
        top_frame = tk.Frame(self.root, bg="#232323")
        top_frame.pack(side="top", fill="x", pady=5)
        self._criar_navbar(top_frame)

        # Área principal (cards + lateral direita)
        main_area = tk.Frame(self.root, bg="#232323")
        main_area.pack(side="top", fill="both", expand=True)

        # Grid de músicas ou playlists
        self.grid_frame = tk.Frame(main_area, bg="#232323")
        self.grid_frame.pack(side="left", fill="both", expand=True, padx=(40, 0), pady=(10, 0))
        self._criar_grid_musicas(self.grid_frame)

        # Lado direito (adicionar música, volume, controles)
        right_frame = tk.Frame(main_area, bg="#232323", width=350)
        right_frame.pack(side="left", fill="y", padx=(30, 0), pady=(0, 0))
        right_frame.pack_propagate(False)

        # Botão Adicionar Música
        self.botao_adicionar = tk.Button(
            right_frame, text="＋ Adicionar Música", font=("Segoe UI", 12),
            bg="#292929", fg="white", relief="flat", activebackground="#444"
        )
        self.botao_adicionar.pack(side="top", fill="x", padx=10, pady=(10, 0))
        self.botao_adicionar.config(command=self._adicionar_musica)

        # Volume e controles na parte inferior
        bottom_controls = tk.Frame(right_frame, bg="#232323")
        bottom_controls.pack(side="bottom", fill="x", pady=30)

        # Volume
        volume_frame = tk.Frame(bottom_controls, bg="#232323")
        volume_frame.pack(side="top", anchor="w", pady=(0, 10))
        tk.Label(volume_frame, text="🔊 Volume", bg="#232323", fg="white", font=("Segoe UI", 11)).pack(side="left", padx=(0, 10))
        self.volume_scale = ttk.Scale(volume_frame, from_=0, to=1, orient=tk.HORIZONTAL, command=self._ajustar_volume, length=200)
        self.volume_scale.set(0.5)
        self.volume_scale.pack(side="left")

        # Controles agrupados e centralizados
        controls_frame = tk.Frame(bottom_controls, bg="#232323")
        controls_frame.pack(side="top", pady=10)

        self.botao_anterior = tk.Button(
            controls_frame, text="⏮ Anterior", font=("Segoe UI", 11),
            bg="#292929", fg="white", relief="flat", width=12,
            activebackground="#444", activeforeground="white", command=self._anterior
        )
        self.botao_anterior.pack(side="left", padx=10)

        self.botao_play_pause = tk.Button(
            controls_frame, text="▶ Play", font=("Segoe UI", 11),
            bg="#292929", fg="white", relief="flat", width=12,
            activebackground="#444", activeforeground="white", command=self._play_pause
        )
        self.botao_play_pause.pack(side="left", padx=10)

        self.botao_proximo = tk.Button(
            controls_frame, text="Próximo ⏭", font=("Segoe UI", 11),
            bg="#292929", fg="white", relief="flat", width=12,
            activebackground="#444", activeforeground="white", command=self._proximo
        )
        self.botao_proximo.pack(side="left", padx=10)

        self._atualizar_musica()
        self.root.mainloop()

    def _criar_navbar(self, parent):
        # Navegação
        nav_items = [
            ("Library", self._abrir_library),
            ("Favoritos", self._abrir_favoritos),
            ("Playlists", self._abrir_playlists),
            ("Configuração", self._abrir_configuracao)
        ]
        self.nav_buttons = []
        for idx, (texto, comando) in enumerate(nav_items):
            btn = tk.Label(
                parent, text=texto, font=("Consolas", 20, "bold" if idx == 0 else "normal"),
                bg="#232323", fg="white", bd=2, relief="solid", padx=16, pady=2
            )
            btn.pack(side="left", padx=(8, 0))
            btn.bind("<Button-1>", lambda e, cmd=comando: cmd())
            self.nav_buttons.append(btn)

        # Espaço entre navegação e busca
        tk.Label(parent, bg="#232323").pack(side="left", padx=20)

        # Campo de busca
        tk.Label(parent, text="Pesquisar", bg="#232323", fg="white", font=("Segoe UI", 12)).pack(side="left")
        self.search_entry = tk.Entry(parent, width=22, font=("Segoe UI", 12), bg="#fff", relief="flat")
        self.search_entry.pack(side="left", padx=(5, 20))

    def _abrir_library(self):
        self.modo_favoritos = False
        self.modo_playlists = False
        self._criar_grid_musicas(self.grid_frame)

    def _abrir_favoritos(self):
        self.modo_favoritos = True
        self.modo_playlists = False
        self._criar_grid_musicas(self.grid_frame)

    def _abrir_playlists(self):
        self.modo_playlists = True
        self._criar_grid_playlists(self.grid_frame)

    def _abrir_configuracao(self):
        self.modo_favoritos = False
        self.modo_playlists = False
        for widget in self.grid_frame.winfo_children():
            widget.destroy()
        tk.Label(self.grid_frame, text="Configurações", fg="white", bg="#232323", font=("Consolas", 22)).pack(pady=40)

    def _atualizar_musica(self):
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

    def _proximo(self):
        self.player.proxima()

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
        self._criar_grid_musicas(self.grid_frame)

    def _criar_grid_musicas(self, parent, musicas=None, playlist_nome=None):
        for widget in parent.winfo_children():
            widget.destroy()

        if musicas is None:
            if self.modo_favoritos:
                musicas = [m for m in self.player.fila if m.caminho_arquivo in self.favoritos]
            else:
                musicas = self.player.fila

        colunas = 4
        card_width = 270
        card_height = 320
        img_size = 170

        # Carregue a imagem do disco uma vez só
        try:
            disco_img = Image.open("disco.png").resize((img_size, img_size))
        except Exception:
            disco_img = Image.new("RGB", (img_size, img_size), color="#ece5c6")
            from PIL import ImageDraw
            draw = ImageDraw.Draw(disco_img)
            draw.ellipse((20, 20, img_size-20, img_size-20), fill="#18343b")
            draw.ellipse((img_size//2-25, img_size//2-25, img_size//2+25, img_size//2+25), fill="#f7b21b")
        disco_img_tk = ImageTk.PhotoImage(disco_img)

        for idx, musica in enumerate(musicas):
            i = idx // colunas
            j = idx % colunas
            card = tk.Frame(parent, bg="#292929", width=card_width, height=card_height)
            card.grid(row=i, column=j, padx=40, pady=20)
            card.pack_propagate(False)

            lbl_img = tk.Label(card, image=disco_img_tk, bg="#ece5c6", width=img_size, height=img_size)
            lbl_img.image = disco_img_tk
            lbl_img.pack(pady=(20, 10))

            tk.Label(card, text=musica.titulo, fg="white", bg="#292929", font=("Consolas", 14, "bold")).pack()
            tk.Label(card, text=musica.artista, fg="#bbbbbb", bg="#292929", font=("Consolas", 12)).pack()

            # Botão de favoritar
            is_fav = musica.caminho_arquivo in self.favoritos
            fav_icon = "★" if is_fav else "☆"
            fav_btn = tk.Button(
                card, text=fav_icon, font=("Segoe UI", 18), fg="#FFD700", bg="#292929",
                relief="flat", bd=0, activebackground="#292929",
                command=lambda m=musica: self._toggle_favorito(m)
            )
            fav_btn.pack(pady=(5, 0))

            # Se estiver em uma playlist, mostrar botões de adicionar/remover
            if playlist_nome:
                btn_remover = tk.Button(
                    card, text="Remover da Playlist", font=("Segoe UI", 9),
                    bg="#444", fg="white", relief="flat",
                    command=lambda m=musica, p=playlist_nome: self._remover_musica_playlist(p, m)
                )
                btn_remover.pack(pady=(5, 0))
            elif self.modo_playlists:
                # Adicionar à playlist selecionada
                for nome in self.playlists:
                    btn_add = tk.Button(
                        card, text=f"Adicionar à {nome}", font=("Segoe UI", 9),
                        bg="#444", fg="white", relief="flat",
                        command=lambda m=musica, p=nome: self._adicionar_musica_playlist(p, m)
                    )
                    btn_add.pack(pady=(2, 0))

            card.bind("<Button-1>", lambda e, m=musica: self._tocar_musica(m))
            for child in card.winfo_children():
                child.bind("<Button-1>", lambda e, m=musica: self._tocar_musica(m))

    def _toggle_favorito(self, musica):
        if musica.caminho_arquivo in self.favoritos:
            self.favoritos.remove(musica.caminho_arquivo)
        else:
            self.favoritos.add(musica.caminho_arquivo)
        self._criar_grid_musicas(self.grid_frame)

    def _tocar_musica(self, musica):
        self.player.tocar(musica)

    # --- PLAYLISTS ---
    def _criar_grid_playlists(self, parent):
        for widget in parent.winfo_children():
            widget.destroy()

        top = tk.Frame(parent, bg="#232323")
        top.pack(side="top", fill="x", pady=10)
        btn_nova = tk.Button(top, text="Nova Playlist", font=("Segoe UI", 12), bg="#292929", fg="white", relief="flat", command=self._criar_playlist)
        btn_nova.pack(side="left", padx=10)
        btn_remover = tk.Button(top, text="Remover Playlist", font=("Segoe UI", 12), bg="#292929", fg="white", relief="flat", command=self._remover_playlist)
        btn_remover.pack(side="left", padx=10)

        # Lista de playlists
        lista_frame = tk.Frame(parent, bg="#232323")
        lista_frame.pack(side="top", fill="both", expand=True, pady=20)

        for idx, nome in enumerate(self.playlists):
            pl_frame = tk.Frame(lista_frame, bg="#292929", width=400, height=60)
            pl_frame.pack(pady=10, padx=40, fill="x")
            pl_frame.pack_propagate(False)
            tk.Label(pl_frame, text=nome, fg="white", bg="#292929", font=("Consolas", 16, "bold")).pack(side="left", padx=20)
            btn_abrir = tk.Button(pl_frame, text="Abrir", font=("Segoe UI", 10), bg="#444", fg="white", relief="flat",
                                  command=lambda n=nome: self._abrir_playlist(n))
            btn_abrir.pack(side="right", padx=10)

    def _criar_playlist(self):
        nome = simpledialog.askstring("Nova Playlist", "Nome da playlist:", parent=self.root)
        if nome and nome not in self.playlists:
            self.playlists[nome] = []
            self._criar_grid_playlists(self.grid_frame)
        elif nome in self.playlists:
            messagebox.showwarning("Aviso", "Já existe uma playlist com esse nome.")

    def _remover_playlist(self):
        if not self.playlists:
            messagebox.showinfo("Info", "Nenhuma playlist para remover.")
            return
        nomes = list(self.playlists.keys())
        nome = simpledialog.askstring("Remover Playlist", f"Digite o nome da playlist para remover:\n{', '.join(nomes)}", parent=self.root)
        if nome in self.playlists:
            del self.playlists[nome]
            self._criar_grid_playlists(self.grid_frame)
        else:
            messagebox.showwarning("Aviso", "Playlist não encontrada.")

    def _abrir_playlist(self, nome):
        # Mostra as músicas da playlist e permite remover
        musicas = self.playlists[nome]
        self._criar_grid_musicas(self.grid_frame, musicas=musicas, playlist_nome=nome)

        # Adicionar botão para adicionar músicas à playlist
        add_frame = tk.Frame(self.grid_frame, bg="#232323")
        add_frame.grid(row=0, column=4, rowspan=2, sticky="n")
        tk.Label(add_frame, text="Adicionar música à playlist:", bg="#232323", fg="white", font=("Consolas", 12)).pack(pady=(10, 5))

        # Lista de músicas que não estão na playlist
        musicas_disponiveis = [m for m in self.player.fila if m not in musicas]
        for musica in musicas_disponiveis:
            btn = tk.Button(
                add_frame,
                text=f"{musica.titulo} - {musica.artista}",
                font=("Segoe UI", 10),
                bg="#292929",
                fg="white",
                relief="flat",
                anchor="w",
                command=lambda m=musica, p=nome: self._adicionar_musica_playlist(p, m)
            )
            btn.pack(fill="x", pady=2, padx=5)

    def _adicionar_musica_playlist(self, playlist_nome, musica):
        if musica not in self.playlists[playlist_nome]:
            self.playlists[playlist_nome].append(musica)
            messagebox.showinfo("Adicionado", f"Música adicionada à playlist '{playlist_nome}'.")
        else:
            messagebox.showwarning("Aviso", "A música já está na playlist.")

    def _remover_musica_playlist(self, playlist_nome, musica):
        if musica in self.playlists[playlist_nome]:
            self.playlists[playlist_nome].remove(musica)
            self._abrir_playlist(playlist_nome)
        else:
            messagebox.showwarning("Aviso", "Música não encontrada na playlist.")
