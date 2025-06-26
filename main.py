from player.player import Player
from interface import InterfaceMusical


player = Player()


app = InterfaceMusical(player)
app.root.mainloop()
