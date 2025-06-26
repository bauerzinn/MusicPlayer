import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from PIL import Image, ImageTk
import pygame
from tkinter import filedialog
from models.musica import Musica
from untils.persistence import carregar_dados, salvar_dados

class InterfaceMusical:
    def __init__(self, player):
        self.player = player


        self.themes = {
            'dark': {
                'bg': '#232323',
                'fg': 'white',
                'card_bg': '#292929',
                'text_secondary': '#bbbbbb',
                'button_bg': '#4a4a4a',
                'button_active': '#666'
            },
            'light': {
                'bg': '#f0f0f0',
                'fg': 'black',
                'card_bg': '#ffffff',
                'text_secondary': '#555555',
                'button_bg': '#e0e0e0',
                'button_active': '#c7c7c7'
            }
        }
        self.theme = 'dark'
        self.themed_widgets = [] 

        # Carregar dados persistidos
        dados_carregados = carregar_dados()
        self.favoritos = dados_carregados["favoritos"]
        self.playlists = dados_carregados["playlists"]
        self.player.fila = dados_carregados["fila"]
        self.player.historico = dados_carregados["historico"]

        self.modo_favoritos = False
        self.modo_playlists = False
        self.criterios = ["Título", "Artista", "Gênero", "Álbum"]

        self.root = tk.Tk()
        self.root.title("SoundWave Music Player")
        self.root.geometry("1500x650")

       
        self.root.protocol("WM_DELETE_WINDOW", self._salvar_e_fechar)

        # Topo: Navegação e busca
        self.top_frame = tk.Frame(self.root)
        self.top_frame.pack(side="top", fill="x", pady=5)
        self._criar_navbar(self.top_frame)

        
        self.combobox_ordenar = ttk.Combobox(
            self.top_frame, values=self.criterios, state="readonly", width=12
        )
        self.combobox_ordenar.set("Título")
        self.combobox_ordenar.pack(side="left", padx=(10, 0))
        self.combobox_ordenar.bind("<<ComboboxSelected>>", self._ordenar_musicas)

        # Área principal (cards + lateral direita)
        self.main_area = tk.Frame(self.root)
        self.main_area.pack(side="top", fill="both", expand=True)

        # Container para o canvas e a scrollbar
        self.grid_container = tk.Frame(self.main_area)
        self.grid_container.pack(side="left", fill="both", expand=True, padx=(40, 0), pady=(10, 0))

        self.canvas = tk.Canvas(self.grid_container, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.grid_container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.root.bind_all("<MouseWheel>", self._on_mousewheel)

        self._criar_grid_musicas(self.scrollable_frame)

        # Lado direito (adicionar música, volume, controles)
        self.right_frame = tk.Frame(self.main_area, width=350)
        self.right_frame.pack(side="left", fill="y", padx=(30, 0), pady=(0, 0))
        self.right_frame.pack_propagate(False)

        # Botão Adicionar Música
        self.botao_adicionar = tk.Button(
            self.right_frame, text="＋ Adicionar Música", font=("Segoe UI", 12),
            relief="flat"
        )
        self.botao_adicionar.pack(side="top", fill="x", padx=10, pady=(10, 0))
        self.botao_adicionar.config(command=self._adicionar_musica)

        # Volume e controles na parte inferior
        self.bottom_controls = tk.Frame(self.right_frame)
        self.bottom_controls.pack(side="bottom", fill="x", pady=30)

        # Volume
        self.volume_frame = tk.Frame(self.bottom_controls)
        self.volume_frame.pack(side="top", anchor="w", pady=(0, 10))
        self.volume_label = tk.Label(self.volume_frame, text="🔊 Volume", font=("Segoe UI", 11))
        self.volume_label.pack(side="left", padx=(0, 10))
        self.volume_scale = ttk.Scale(self.volume_frame, from_=0, to=1, orient=tk.HORIZONTAL, command=self._ajustar_volume, length=200)
        self.volume_scale.set(0.5)
        self.volume_scale.pack(side="left")

        self.controls_frame = tk.Frame(self.bottom_controls)
        self.controls_frame.pack(side="top", pady=10)

        self.botao_anterior = tk.Button(
            self.controls_frame, text="⏮ Anterior", font=("Segoe UI", 11),
            relief="flat", width=12, command=self._anterior
        )
        self.botao_anterior.pack(side="left", padx=10)

        self.botao_play_pause = tk.Button(
            self.controls_frame, text="▶ Play", font=("Segoe UI", 11),
            relief="flat", width=12, command=self._play_pause
        )
        self.botao_play_pause.pack(side="left", padx=10)

        self.botao_proximo = tk.Button(
            self.controls_frame, text="⏭ Próximo", font=("Segoe UI", 11),
            relief="flat", width=12, command=self._proximo
        )
        self.botao_proximo.pack(side="left", padx=10)

        self.themed_widgets.extend([
            self.root, self.top_frame, self.main_area, self.grid_container, self.canvas, 
            self.scrollable_frame, self.right_frame, self.botao_adicionar, self.bottom_controls, 
            self.volume_frame, self.volume_label, self.controls_frame, self.botao_anterior, 
            self.botao_play_pause, self.botao_proximo
        ])

        self._apply_theme()

    def run(self):
        self._atualizar_musica()
        self.root.mainloop()

    def _on_mousewheel(self, event):
        """Permite rolar la lista de músicas com o scroll do mouse."""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _salvar_e_fechar(self):
        salvar_dados(self.player, self.playlists, self.favoritos)
        self.root.destroy()

    def _criar_navbar(self, parent):
        # Navegação
        nav_items = [
            ("Library", self._abrir_library),
            ("Favoritos", self._abrir_favoritos),
            ("Playlists", self._abrir_playlists),
            ("Histórico", self._abrir_historico),
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

        tk.Label(parent, bg="#232323").pack(side="left", padx=20)

        # Campo de busca
        tk.Label(parent, text="Pesquisar", bg="#232323", fg="white", font=("Segoe UI", 12)).pack(side="left")
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(parent, width=22, font=("Segoe UI", 12), bg="#fff", relief="flat", textvariable=self.search_var)
        self.search_entry.pack(side="left", padx=(5, 20))
        self.search_entry.bind("<KeyRelease>", self._buscar_musicas)

    def _abrir_library(self):
        self.modo_favoritos = False
        self.modo_playlists = False
        self._criar_grid_musicas(self.scrollable_frame)

    def _abrir_favoritos(self):
        self.modo_favoritos = True
        self.modo_playlists = False
        musicas_favoritas = [m for m in self.player.fila if m.caminho_arquivo in self.favoritos]
        self._criar_grid_musicas(self.scrollable_frame, musicas=musicas_favoritas)

    def _abrir_playlists(self):
        self.modo_playlists = True
        self.modo_favoritos = False
        self._criar_grid_playlists(self.scrollable_frame)

    def _abrir_configuracao(self):
        self.modo_favoritos = False
        self.modo_playlists = False
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        colors = self.themes[self.theme]

        tk.Label(self.scrollable_frame, text="Configurações", fg=colors['fg'], bg=colors['bg'], font=("Consolas", 22)).pack(pady=40)

        # Botão para alternar tema
        theme_button_text = "Mudar para Tema Claro" if self.theme == 'dark' else "Mudar para Tema Escuro"
        self.theme_button = tk.Button(
            self.scrollable_frame, 
            text=theme_button_text, 
            command=self._toggle_theme, 
            font=("Segoe UI", 12),
            bg=colors['button_bg'], 
            fg=colors['fg'], 
            activebackground=colors['button_active'],
            relief="flat"
        )
        self.theme_button.pack(pady=20)

    def _toggle_theme(self):
        """Alterna entre o tema claro e escuro."""
        self.theme = 'light' if self.theme == 'dark' else 'dark'
        self._apply_theme()
        self._abrir_configuracao() # Redesenha a página de configurações para atualizar o botão

    def _apply_theme(self):
        colors = self.themes[self.theme]
        button_config = {
            'bg': colors['button_bg'],
            'fg': colors['fg'],
            'activebackground': colors['button_active'],
            'activeforeground': colors['fg']
        }

        for widget in self.themed_widgets:
            try:
                widget.configure(bg=colors['bg'])
            except tk.TclError:
                pass

        self.botao_adicionar.config(**button_config)
        self.botao_anterior.config(**button_config)
        self.botao_play_pause.config(**button_config)
        self.botao_proximo.config(**button_config)
        self.volume_label.config(fg=colors['fg'])

        for child in self.top_frame.winfo_children():
            if isinstance(child, tk.Button):
                child.config(bg=colors['bg'], fg=colors['fg'], activebackground=colors['button_active'])

    def _abrir_historico(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        tk.Label(self.scrollable_frame, text="Histórico de Músicas", fg="white", bg="#232323", font=("Consolas", 22)).pack(pady=20)
        historico = self.player.ver_historico()
        if not historico:
            tk.Label(self.scrollable_frame, text="Nenhuma música reproduzida ainda.", fg="#bbbbbb", bg="#232323", font=("Consolas", 14)).pack(pady=10)
            return
        for musica in historico:
            frame = tk.Frame(self.scrollable_frame, bg="#292929")
            frame.pack(fill="x", padx=40, pady=5)
            tk.Label(frame, text=musica.titulo, fg="white", bg="#292929", font=("Consolas", 14, "bold")).pack(side="left", padx=10)
            tk.Label(frame, text=musica.artista, fg="#bbbbbb", bg="#292929", font=("Consolas", 12)).pack(side="left", padx=10)

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
        self._criar_grid_musicas(self.scrollable_frame)

    def _criar_grid_musicas(self, parent, musicas=None, playlist_nome=None):
        for widget in parent.winfo_children():
            widget.destroy()

        if musicas is None:
            if self.modo_favoritos:
                musicas = [m for m in self.player.fila if m.caminho_arquivo in self.favoritos]
            else:
                musicas = self.player.fila

        cols = 5
        for i, musica in enumerate(musicas):
            row, col = divmod(i, cols)

            card = tk.Frame(parent, bd=1, relief="solid", borderwidth=0, width=220, height=320)
            card.grid(row=row, column=col, padx=15, pady=15)
            card.pack_propagate(False)

            click_handler = lambda e, m=musica: self._tocar_musica(m)
            card.bind("<Button-1>", click_handler)

            colors = self.themes[self.theme]
            card.config(bg=colors['card_bg'])

            # Imagem do disco
            disco_img = Image.open("disco.png").resize((150, 150), Image.Resampling.LANCZOS)
            disco_img_tk = ImageTk.PhotoImage(disco_img)
            lbl_img = tk.Label(card, image=disco_img_tk, bg=colors['card_bg'])
            lbl_img.image = disco_img_tk
            lbl_img.pack(pady=(20, 10))
            lbl_img.bind("<Button-1>", click_handler)

            title_label = tk.Label(card, text=musica.titulo, font=("Consolas", 14, "bold"), fg=colors['fg'], bg=colors['card_bg'])
            title_label.pack()
            title_label.bind("<Button-1>", click_handler)

            artist_label = tk.Label(card, text=musica.artista, font=("Consolas", 12), fg=colors['text_secondary'], bg=colors['card_bg'])
            artist_label.pack(pady=(0, 10))
            artist_label.bind("<Button-1>", click_handler)

            actions_frame = tk.Frame(card, bg=colors['card_bg'])
            actions_frame.pack(pady=5)

            # Botão de favorito
            fav_char = "★" if musica.caminho_arquivo in self.favoritos else "☆"
            fav_btn = tk.Button(
                actions_frame, text=fav_char, font=("Segoe UI", 16, "bold"), fg="#FFD700",
                bg=colors['card_bg'], relief="flat", bd=0, activebackground=colors['card_bg'],
                command=lambda m=musica: self._toggle_favorito(m)
            )
            fav_btn.pack(side="left", padx=10)

            # Botão de editar
            edit_button = tk.Button(
                actions_frame, text="Editar", font=("Segoe UI", 10),
                bg=colors['button_bg'], fg=colors['fg'],
                relief="flat", activebackground=colors['button_active'],
                command=lambda m=musica: self._editar_musica(m)
            )
            edit_button.pack(side="left", padx=10)

            # Se estiver em uma playlist, mostrar botão de remover
            if playlist_nome:
                remover_musica_btn = tk.Button(
                    actions_frame, text="Remover", font=("Segoe UI", 10),
                    bg="#5a2a2a", fg="white", relief="flat", activebackground="#7a4a4a",
                    command=lambda p=playlist_nome, m=musica: self._remover_musica_playlist(p, m)
                )
                remover_musica_btn.pack(side="left", padx=10)

    def _toggle_favorito(self, musica):
        caminho = musica.caminho_arquivo
        if caminho in self.favoritos:
            self.favoritos.remove(caminho)
        else:
            self.favoritos.add(caminho)
        self._criar_grid_musicas(self.scrollable_frame)

    def _editar_musica(self, musica):
        editor_window = tk.Toplevel(self.root)
        editor_window.title("Editar Música")
        editor_window.geometry("400x250")
        editor_window.configure(bg="#232323")
        editor_window.resizable(False, False)

        x = self.root.winfo_x()
        y = self.root.winfo_y()
        editor_window.geometry(f"+{(x + self.root.winfo_width() // 2) - 200}+{(y + self.root.winfo_height() // 2) - 125}")

        colors = self.themes[self.theme]
        editor_window.configure(bg=colors['bg'])

        frame = tk.Frame(editor_window, padx=20, pady=20, bg=colors['bg'])
        frame.pack(fill="both", expand=True)

        # Campos de entrada
        tk.Label(frame, text="Título:", font=("Segoe UI", 11), bg=colors['bg'], fg=colors['fg']).grid(row=0, column=0, sticky="w", pady=5)
        titulo_var = tk.StringVar(value=musica.titulo)
        tk.Entry(frame, textvariable=titulo_var, width=40, bg=colors['button_bg'], fg=colors['fg'], relief="flat").grid(row=0, column=1, sticky="w")

        tk.Label(frame, text="Artista:", font=("Segoe UI", 11), bg=colors['bg'], fg=colors['fg']).grid(row=1, column=0, sticky="w", pady=5)
        artista_var = tk.StringVar(value=musica.artista)
        tk.Entry(frame, textvariable=artista_var, width=40, bg=colors['button_bg'], fg=colors['fg'], relief="flat").grid(row=1, column=1, sticky="w")

        tk.Label(frame, text="Gênero:", font=("Segoe UI", 11), bg=colors['bg'], fg=colors['fg']).grid(row=2, column=0, sticky="w", pady=5)
        genero_var = tk.StringVar(value=musica.genero)
        tk.Entry(frame, textvariable=genero_var, width=40, bg=colors['button_bg'], fg=colors['fg'], relief="flat").grid(row=2, column=1, sticky="w")

        def salvar_edicao():
            musica.titulo = titulo_var.get()
            musica.artista = artista_var.get()
            musica.genero = genero_var.get()
            editor_window.destroy()
            self._criar_grid_musicas(self.scrollable_frame)

        # Botão Salvar
        save_button = tk.Button(frame, text="Salvar", command=salvar_edicao, font=("Segoe UI", 11), bg=colors['button_bg'], fg=colors['fg'], relief="flat")
        save_button.grid(row=3, column=1, sticky="e", pady=20)

        editor_window.transient(self.root)
        editor_window.grab_set()
        self.root.wait_window(editor_window)

    def _tocar_musica(self, musica):
        self.player.tocar(musica)

    def _criar_grid_playlists(self, parent):
        for widget in parent.winfo_children():
            widget.destroy()

        top = tk.Frame(parent, bg="#232323")
        top.pack(side="top", fill="x", pady=10)
        btn_nova = tk.Button(top, text="Nova Playlist", font=("Segoe UI", 12), bg="#292929", fg="white", relief="flat", command=self._criar_playlist)
        btn_nova.pack(side="left", padx=10)
        btn_remover = tk.Button(top, text="Remover Playlist", font=("Segoe UI", 12), bg="#292929", fg="white", relief="flat", command=self._remover_playlist)
        btn_remover.pack(side="left", padx=10)

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
        nome = simpledialog.askstring("Nova Playlist", "Digite o nome da playlist:", parent=self.root)
        if nome and nome not in self.playlists:
            self.playlists[nome] = []
            self._criar_grid_playlists(self.scrollable_frame)
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
            self._criar_grid_playlists(self.scrollable_frame)
        else:
            messagebox.showwarning("Aviso", "Playlist não encontrada.")

    def _abrir_playlist(self, nome):
        musicas = self.playlists[nome]
        self._criar_grid_musicas(self.scrollable_frame, musicas=musicas, playlist_nome=nome)

        add_frame = tk.Frame(self.scrollable_frame, bg="#232323")
        add_frame.grid(row=0, column=4, rowspan=2, sticky="n")
        tk.Label(add_frame, text="Adicionar música à playlist:", bg="#232323", fg="white", font=("Consolas", 12)).pack(pady=(10, 5))

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

    def _ordenar_musicas(self, event=None):
        criterio = self.combobox_ordenar.get().lower()
        if self.modo_favoritos:
            musicas = [m for m in self.player.fila if m.caminho_arquivo in self.favoritos]
        elif self.modo_playlists:
            return
        else:
            musicas = self.player.fila

        if criterio == "título":
            musicas.sort(key=lambda m: m.titulo)
        elif criterio == "artista":
            musicas.sort(key=lambda m: m.artista)
        elif criterio == "gênero":
            musicas.sort(key=lambda m: m.genero)
        elif criterio == "álbum":
            musicas.sort(key=lambda m: m.album)

        self._criar_grid_musicas(self.scrollable_frame, musicas=musicas)

    def _buscar_musicas(self, event=None):
        termo = self.search_var.get().lower()
        if self.modo_favoritos:
            musicas = [m for m in self.player.fila if m.caminho_arquivo in self.favoritos]
        elif self.modo_playlists:
            return
        else:
            musicas = self.player.fila

        if termo:
            musicas_filtradas = [
                m for m in musicas
                if termo in m.titulo.lower()
                or termo in m.artista.lower()
                or termo in m.genero.lower()
                or termo in m.album.lower()
            ]
        else:
            musicas_filtradas = musicas

        self._criar_grid_musicas(self.scrollable_frame, musicas=musicas_filtradas)
