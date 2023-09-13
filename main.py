from game.scrabble_game import ScrabbleGame
from game.models import Board, Player, Tiles, Cell

def main(self):
    while True:
        try:
            players_count = int(input('Cantidad de jugadores:'))
            if players_count < 1 or players_count > 4:
                raise ValueError
            break
        except ValueError:
            print("Valor Invalido")
    
    game = ScrabbleGame(players_count)
    board = Board()
    board.positions()
    word = input("Ingrese Palabra:")
    location_i = input("Ingrese X: ")
    location_j = input("Ingrese Y: ")
    location = (location_i, location_j)
    orientation = input ("Orientacion V o H: ")
    while(game.playing()):
        pass