#!/usr/bin/env python3.10
from game.scrabble_game import ScrabbleGame
from game.models import Player, Tiles, Cell
from game.board import Board


def main():
    while True:
        try:
            players_count = int(input('Cantidad de jugadores:'))
            if players_count < 1 or players_count > 4:
                raise ValueError
            break
        except ValueError:
            print("Valor Invalido")
    
    game = ScrabbleGame(players_count)
    while(game.playing()):
        task = input("Para agregar palabra ingrese A",
                     "Para cambiar letras ingrese C",
                     "Para pasar de turno ingrese P")
        task.upper()
        if task == "A":
            word = input("Ingrese Palabra:")
            location_i = input("Ingrese X: ")
            location_j = input("Ingrese Y: ")
            location = (location_i, location_j)
            orientation = input ("Orientacion V o H: ")
            game.playing(word, location, orientation)
        elif task == "C":
            pass
        elif task == "P":
            game.next_turn()

if __name__ == '__main__':
    main()

    """

    El jugador puede:
    1- Agregar palabras
    2- Cambiar fichas
    3- Pasar de turno

    Despues de agregar la palabra
    1- Verifico que el board o este vacio o la palabara pase por (7, 7)
    2- Verifico que la palabra no este en el tablero
    3- Verifico el lugar en el board, que no este fuera de rango
    4- Verifico que el jugador tenga los Tiles
    5- Verifico que la palabra cruce o anada letras a otra palabra
    6- Verifico que la palabra/palabras existan
    7- Calculo el valor 
    8- Agrego la palabra al board y a la lista de palabras
    9- Cambio de turno 
    """