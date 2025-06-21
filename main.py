from player.player import Player
from interface import InterfaceMusical

# Inicializar player
player = Player()

# Iniciar interface gráfica
app = InterfaceMusical(player)
app.root.mainloop()  # O loop principal agora é chamado aqui
