from game.scrabble_game import ScrabbleGame

def main(self):
    player_count = int(input('Cantidad de jugadores:'))
    game = ScrabbleGame(player_count)
    while(game.playing()):
        pass